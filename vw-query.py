import tree
import tparser
import features
import subprocess, random, socket
import time
import os.path
import sys
import select
import cPickle as pickle
import codecs

"""
  This module allows us to query VW. It is the most horrible hack ever
  because we need to get the raw predicitions in multiclass and VW
  writes these into a file only. So the setup is as follows:

  - start VW in the daemon mode and use the TCP connection to feed it
    examples 

  - use a named pipe as the output file for the VW raw
    predictions, and read from it after every TCP connection, hoping
    everything gets flushed in time

  We want to avoid restarting VW for every prediction at any cost,
  because we need to make at least twice as many predictions as we
  have tokens to parse, and in a beam search scenario, it gets even
  much, much worse.

"""

THIS=os.path.dirname(os.path.abspath(__file__))

def sanitize(f):
    return f.replace(u":",u"__colon__").replace(u"|",u"__bar__")


class VWQuery(object):

    def __init__(self,model_file):
        fifo_pipe_name=os.path.join(THIS,"vw_raw_out.pipe")
        if not os.path.exists(fifo_pipe_name):
            os.system("mkfifo --mode 0666 "+fifo_pipe_name)
        os.system("dd if=%s iflag=nonblock of=/dev/null"%fifo_pipe_name) #Flush the pipe
        self.port=random.randint(10000,55000)
        vwCMD="/usr/local/bin/vw -t -i %s --daemon --port %d -r %s --quiet"%(model_file,self.port,fifo_pipe_name)
        self.vw=subprocess.Popen(vwCMD,shell=True)
        self.raw_pred_read=open(fifo_pipe_name,"rt")              
        #while self.raw_pred_read in select.select([self.raw_pred_read],[],[],0.2):
        #    self.raw_pred_read.readline() #Consume the pipe
        while True:
            try:
                time.sleep(1) #wait a sec so VW has the time to start and open the socket
                self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(('127.0.0.1',self.port))
                break
            except socket.error:
                print >> sys.stderr, "Retrying connection. Model probably not yet loaded"
        self.build_class2tr_dict()

    def build_class2tr_dict(self):
        self.cls2transition={} #VW class number -> Transition()
        with open("vw_classes.pkl","rb") as f:
            class_dict=pickle.load(f)
            for tr_string, cls_num in class_dict.iteritems():
                move,depType=tr_string.split(":")
                move=int(move)
                if depType=="None":
                    depType=None
                assert cls_num not in self.cls2transition
                trans=tparser.Transition(move,depType)
                self.cls2transition[cls_num]=trans

    def __del__(self):
        self.vw.kill()
        os.system("ps x | grep vw | grep 'daemon --port %d -r ' | cut -f 1 -d\ | xargs kill"%(self.port))
        self.raw_pred_read.close()
        self.sock.close()

    def query(self,feat_line):
        self.sock.sendall("| "+feat_line+"\n")
        cls = int(float(self.sock.recv(1024))) #we get the class as a float for some reason "7.00000"
        weights=self.raw_pred_read.readline()  # "1:2.38897 2:-1.57863 3:-1.78991 4:-1.49548"
        class_weights=[] #[(class,weight), (class,weight), ...]
        for cls_w in weights.split():
            c,w=cls_w.split(":")
            class_weights.append((int(c),float(w)))
        class_weights.sort(reverse=True,key=lambda x: x[1])
        assert cls==class_weights[0][0], (cls, class_weights)
        return class_weights

    def det_parse_conll(self):
        out=codecs.getwriter("utf-8")(sys.stdout)
        feature_gen=features.Features()
        for sent in tree.read_conll("/dev/stdin"):
            #t=tree.Tree(None,conll=sent,syn=False,conll_format="conll09")  ###? do I need this?
            initial_state=tparser.State(None,sent)
            finished=self.det_parse(initial_state,feature_gen)
            tree.fill_conll(sent,finished)
            tree.write_conll(out,sent)

    def det_parse(self, state, feature_gen):
        shift_tr=tparser.Transition(tparser.SHIFT,None)
        #Now do shift-shift to start the parsing
        state.update(shift_tr)
        if state.valid_transitions():
            state.update(shift_tr)
        else:
            return state
        while True:
            valid_moves=state.valid_transitions() #set(t.move for t in state.valid_transitions())
            if not valid_moves:
                #DONE!
                return state

            feats=feature_gen.create_features(state)
            feat_line=(u" ".join(sanitize(f)+u":"+unicode(v) for f,v in feats.iteritems())).encode("utf-8")
            weights=self.query(feat_line)
#            print weights[:4], feat_line
            for cls,w in weights:
                transition=self.cls2transition[cls]
                if transition.move in valid_moves: #Go!
                    state.update(transition)
                    break
            else: #What? No transition valid?
                assert False #should never, ever happen. Never.
                
if __name__=="__main__":
    q=VWQuery("/home/ginter/Turku-Dependency-Parser/trained-pb-sngrams.vw")
    q.det_parse_conll()
    sys.exit()
    tot=0
    cr=0
    err={}
    with open("tdt-test.vwdata","rt") as f:
        for line in f:
            line=line.strip()
            cls,feat=line.split("|",1)
            weights=q.query(feat)
            pcls=weights[0][0]
            if int(cls)==pcls:
                cr+=1
            else:
                err[(cls,pcls)]=err.get((cls,pcls),0)+1
            tot+=1
            if tot%10000==0:
                print float(cr)/tot
            if tot%100000==0:
                break
    errors=err.items()
    errors.sort(key=lambda x: x[1], reverse=True)
    print errors[:20]

            
            

