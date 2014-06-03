import tree, tparser
import sys
import cPickle as pickle
import traceback
import time
import features

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

def tree_compare(t1,t2):
    #Check that two trees are the same
    assert len(t1.tokens)==len(t2.tokens), (t1.tokens,t2.tokens)
    heads1=[None for _ in range(len(t1.tokens))]
    heads2=[None for _ in range(len(t2.tokens))]
    for t1dep in t1.deps:
        heads1[t1dep.dep.index]=(t1dep.gov.index,t1dep.dType)
    for t2dep in t2.deps:
        heads2[t2dep.dep.index]=(t2dep.gov.index,t2dep.dType)
    if heads1!=heads2:
        print t1.tokens
        print heads1
        print heads2
    return heads1==heads2


def token_feats(ns,prefix,token,d):
    d[ns.lower()][u"%s.form_%s"%(prefix,token.text.lower())]=1
    d[ns.upper()][u"%s.pos_%s"%(prefix,token.pos)]=1
    d[ns.upper()][u"%s.lemma_%s"%(prefix,token.lemma)]=1
    if token.feat!=u"_":
        for f_v in token.feat.split(u"|"):
            d[ns.lower()][u"%s.feat_%s"%(prefix,f_v)]=1
    else:
        d[ns.lower()][u"%s.feat_empty"%prefix]=1
        
def sanitize(f):
    return f.replace(u":",u"__colon__").replace(u"|",u"__bar__")

def get_state_features(s):
    d={u"S":{},u"s":{},u"Q":{},u"q":{}} #VW feature namespaces, they must be single-letter (sigh)
    for idx in range(2):
        if idx<len(s.stack):
            token_feats(u"s",u"S%d"%idx,s.stack[idx],d)
        else:
            d["S"][u"S%d_empty"%idx]=1
    for idx in range(3):
        if idx<len(s.queue):
            token_feats(u"q",u"Q%d"%idx,s.queue[idx],d)
        else:
            d[u"Q"][u"Q%d_empty"%idx]=1
    return d

def one_sent_example(sent,parser,feature_gen):
    shift_t=tparser.Transition(tparser.SHIFT,None)
    if len(sent)<2:
        return
    t=tree.Tree.new_from_conll(sent,syn=True)
    non_projs=t.is_nonprojective()
    if len(non_projs)>0:
        t.define_projective_order(non_projs)
    gs_transitions=parser.extract_transitions(t,sent)
    state=tparser.State(sent,syn=False)
    for tr_idx,tr in enumerate(gs_transitions):
        try:
            cls=get_cls_num(str(tr),False)
        except KeyError:
            pass
        if tr_idx>2: #Don't generate features for the first three shifts because those are automatic
            feats=feature_gen.create_features(state)
            print cls, u"  ", 
            print u"|", (u" ".join(sanitize(f)+u":"+str(v) for f,v in feats.iteritems())).encode("utf-8")
        state.update(tr)

if __name__=="__main__":
    fg=features.Features()
    start=time.time()
    sent_OK,sent_TOT=0,0
    p=tparser.Parser()
    for sent in tree.read_conll("/dev/stdin"):
        if sent_TOT==3000000:
            break
        sent_TOT+=1
        if sent_TOT%1000==0:
            elapsed=time.time()-start
            print >> sys.stderr, "Processed sentences ok/total:", sent_OK, "/", sent_TOT, "     ", sent_TOT/elapsed, "sent/sec"
            sys.stderr.flush()
            sys.stdout.flush()
        try:
            one_sent_example(sent,p,fg)
            sent_OK+=1
        except ValueError:
            pass


