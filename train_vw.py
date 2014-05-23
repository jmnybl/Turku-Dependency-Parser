import tree, tparser
import sys
import cPickle as pickle
import traceback

class_dict={}

def get_cls_num(cls):
    global class_dict
    if cls in class_dict:
        return class_dict[cls]
    else:
        n=len(class_dict)+1
        class_dict[cls]=n
        with open("vw_classes.pkl","wb") as f:
            pickle.dump(class_dict,f,pickle.HIGHEST_PROTOCOL)
        return n

def token_feats(prefix,token,d):
    if token:
        d[u"%s.form_%s"%(prefix,token.text)]=1
        d[u"%s.pos_%s"%(prefix,token.pos)]=1
        d[u"%s.lemma_%s"%(prefix,token.lemma)]=1
    else:
        d[u"%s.form_None"%(prefix)]=1
        d[u"%s.pos_None"%(prefix)]=1
        d[u"%s.lemma_None"%(prefix)]=1


def get_state_features(s):
    d={}
    for idx in range(3):
        if idx<len(s.stack):
            token_feats("S%d"%idx,s.stack[idx],d)
        else:
            token_feats("S%d"%idx,None,d)
    for idx in range(3):
        if idx<len(s.queue):
            token_feats("Q%d"%idx,s.queue[idx],d)
        else:
            token_feats("Q%d"%idx,None,d)
    return d

def one_sent_example(sent,parser):
    if len(sent)<2:
        return
    tokens=u" ".join(t[1] for t in sent)
    t=tree.Tree(tokens,conll=sent,syn=True,conll_format="conll09")
    non_projs=t.is_nonprojective()
    if len(non_projs)>0:
        t.define_projective_order(non_projs)
    gs_transitions=parser.extract_transitions(t,tokens)
    state=tparser.State(tokens)
    for tr in gs_transitions:
        cls=get_cls_num(str(tr))
        feats=get_state_features(state)
        print cls, u"|", (u" ".join(f for f in feats)).encode("utf-8")
        state.update(tr)

if __name__=="__main__":
    p=tparser.Parser()
    for sent in tree.read_conll("/dev/stdin"):
        try:
            one_sent_example(sent,p)
        except ValueError:
            traceback.print_exc()


