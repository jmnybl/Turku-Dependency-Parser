import tree, tparser
import sys
import cPickle as pickle
import traceback
import time

with open("vw_classes.pkl","rb") as f:
    class_dict=pickle.load(f)

def get_cls_num(cls,update=False):
    global class_dict
    if cls in class_dict:
        return class_dict[cls]
    elif update:
        n=len(class_dict)+1
        class_dict[cls]=n
        with open("vw_classes.pkl","wb") as f:
            pickle.dump(class_dict,f,pickle.HIGHEST_PROTOCOL)
        return n
    else:
        raise KeyError(cls)

def token_feats(ns,prefix,token,d):
    d[ns.lower()][u"%s.form_%s"%(prefix,token.text)]=1
    d[ns.upper()][u"%s.pos_%s"%(prefix,token.pos)]=1
    d[ns.upper()][u"%s.lemma_%s"%(prefix,token.lemma)]=1
    if token.feat!=u"_":
        for f_v in token.feat.split(u"|"):
            d[ns.lower()][u"%s.feat_%s"%(prefix,f_v)]=1
        

def sanitize(f):
    return f.replace(u":",u"__colon__").replace(u"|",u"__bar__")

def get_state_features(s):
    d={u"S":{},u"s":{},u"Q":{},u"q":{}}
    for idx in range(3):
        if idx<len(s.stack):
            token_feats(u"s",u"S%d"%idx,s.stack[idx],d)
        else:
            d["S"][u"S%d_empty"%idx]=1
    for idx in range(4):
        if idx<len(s.queue):
            token_feats(u"q",u"Q%d"%idx,s.queue[idx],d)
        else:
            d[u"Q"][u"Q%d_empty"%idx]=1
    return d

def one_sent_example(sent,parser):
    if len(sent)<2:
        return
    tokens=u" ".join(t[1] for t in sent)
    t=tree.Tree(None,conll=sent,syn=True,conll_format="conll09")
    non_projs=t.is_nonprojective()
    if len(non_projs)>0:
        t.define_projective_order(non_projs)
    gs_transitions=parser.extract_transitions(t,tokens)
    state=tparser.State(None,sent)
    for tr in gs_transitions:
        try:
            cls=get_cls_num(str(tr),False)
        except KeyError:
            continue
        feats=get_state_features(state)
        print cls, u"  ", 
        for namespace, fDict in feats.iteritems():
            print u"|"+namespace, (u" ".join(sanitize(f) for f in fDict)).encode("utf-8"),u" ",
        print

        state.update(tr)

if __name__=="__main__":
    start=time.time()
    sent_OK,sent_TOT=0,0
    p=tparser.Parser()
    for sent in tree.read_conll("/dev/stdin"):
        if sent_TOT==5000000:
            break
        sent_TOT+=1
        if sent_TOT%1000==0:
            elapsed=time.time()-start
            print >> sys.stderr, "Processed sentences ok/total:", sent_OK, "/", sent_TOT, "     ", sent_TOT/elapsed, "sent/sec"
            sys.stderr.flush()
            sys.stdout.flush()
        try:
            one_sent_example(sent,p)
            sent_OK+=1
        except ValueError:
            pass


