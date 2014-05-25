import subprocess, random, socket
import time
import os.path

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

class VWQuery(object):

    def __init__(self,model_file):
        fifo_pipe_name=os.path.join(THIS,"vw_raw_out.pipe")
        if not os.path.exists(fifo_pipe_name):
            os.system("mkfifo --mode 0666 "+fifo_pipe_name)
        self.port=random.randint(10000,55000)
        vwCMD="/usr/local/bin/vw -t -i %s -q QS -q QQ -q SS -q Qs -q qS --daemon --port %d -r %s --quiet"%(model_file,self.port,fifo_pipe_name)
        self.vw=subprocess.Popen(vwCMD,shell=True)
        self.raw_pred_read=open(fifo_pipe_name,"rt")              
        time.sleep(1) #wait a sec so VW has the time to start and open the socket
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1',self.port))


    def __del__(self):
        self.vw.kill()
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

if __name__=="__main__":
    q=VWQuery("/home/ginter/Turku-Dependency-Parser/trained.vw.0")
    tot=0
    cr=0
    with open("out/pbv3.part-07.gz.vwdata","rt") as f:
        for line in f:
            line=line.strip()
            cls,feat=line.split("|",1)
            weights=q.query(feat)
            pcls=weights[0][0]
            if int(cls)==pcls:
                cr+=1
            tot+=1
            if tot%10000==0:
                print float(cr)/tot

            
            

