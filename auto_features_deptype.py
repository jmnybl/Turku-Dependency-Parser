
def get_child(token,idx,state):
    if token is None: return None
    childs=sorted(state.tree.childs[token], key=lambda x:x.index)
    if len(childs)>0:
        if idx==u"ld": # leftmost
            return childs[0]
        elif idx==u"rd": # rightmost
            return childs[-1]
        else:
            index=int(idx[1])
            if idx>len(childs)-1: return None
            return childs[index]
    else:
        return None



def get_from_stack(stack):
    if len(stack)>2:
        return stack[-1],stack[-2],stack[-3]
    elif len(stack)>1:
        return stack[-1],stack[-2],None
    elif len(stack)>0:
        return stack[-1],None,None
    else:
        return None,None,None



def create_auto_dep_features(state):
    S0,S1,S2=get_from_stack(state.stack)
    features={}
    d1_S0_=get_child(S0,'d1',state)
    rd_S0_=get_child(S0,'rd',state)
    d2_S0_=get_child(S0,'d2',state)
    ld_S2_=get_child(S2,'ld',state)
    ld_S0_=get_child(S0,'ld',state)
    d0_S1_=get_child(S1,'d0',state)
    rd_S2_=get_child(S2,'rd',state)
    d0_S0_=get_child(S0,'d0',state)
    d2_S1_=get_child(S1,'d2',state)
    d1_S1_=get_child(S1,'d1',state)
    ld_S1_=get_child(S1,'ld',state)
    rd_S1_=get_child(S1,'rd',state)
    if (ld_S0_ is not None) and (S0 is not None) and (S0 is not None) :
        features['d(ld(S0))p(S0)p(S0)='+str(state.tree.dtypes.get(ld_S0_))+S0.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S1 is not None) :
        features['d(ld(S0))p(S0)p(S1)='+str(state.tree.dtypes.get(ld_S0_))+S0.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S2 is not None) :
        features['d(ld(S0))p(S0)p(S2)='+str(state.tree.dtypes.get(ld_S0_))+S0.pos+S2.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S0 is not None) :
        features['d(ld(S0))p(S1)p(S0)='+str(state.tree.dtypes.get(ld_S0_))+S1.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S1 is not None) :
        features['d(ld(S0))p(S1)p(S1)='+str(state.tree.dtypes.get(ld_S0_))+S1.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S2 is not None) :
        features['d(ld(S0))p(S1)p(S2)='+str(state.tree.dtypes.get(ld_S0_))+S1.pos+S2.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S0 is not None) :
        features['d(ld(S0))p(S2)p(S0)='+str(state.tree.dtypes.get(ld_S0_))+S2.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S1 is not None) :
        features['d(ld(S0))p(S2)p(S1)='+str(state.tree.dtypes.get(ld_S0_))+S2.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S2 is not None) :
        features['d(ld(S0))p(S2)p(S2)='+str(state.tree.dtypes.get(ld_S0_))+S2.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S0 is not None) :
        features['d(ld(S1))p(S0)p(S0)='+str(state.tree.dtypes.get(ld_S1_))+S0.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S1 is not None) :
        features['d(ld(S1))p(S0)p(S1)='+str(state.tree.dtypes.get(ld_S1_))+S0.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S2 is not None) :
        features['d(ld(S1))p(S0)p(S2)='+str(state.tree.dtypes.get(ld_S1_))+S0.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S0 is not None) :
        features['d(ld(S1))p(S1)p(S0)='+str(state.tree.dtypes.get(ld_S1_))+S1.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S1 is not None) :
        features['d(ld(S1))p(S1)p(S1)='+str(state.tree.dtypes.get(ld_S1_))+S1.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S2 is not None) :
        features['d(ld(S1))p(S1)p(S2)='+str(state.tree.dtypes.get(ld_S1_))+S1.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S0 is not None) :
        features['d(ld(S1))p(S2)p(S0)='+str(state.tree.dtypes.get(ld_S1_))+S2.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S1 is not None) :
        features['d(ld(S1))p(S2)p(S1)='+str(state.tree.dtypes.get(ld_S1_))+S2.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S2 is not None) :
        features['d(ld(S1))p(S2)p(S2)='+str(state.tree.dtypes.get(ld_S1_))+S2.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S0 is not None) :
        features['d(ld(S2))p(S0)p(S0)='+str(state.tree.dtypes.get(ld_S2_))+S0.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S1 is not None) :
        features['d(ld(S2))p(S0)p(S1)='+str(state.tree.dtypes.get(ld_S2_))+S0.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S2 is not None) :
        features['d(ld(S2))p(S0)p(S2)='+str(state.tree.dtypes.get(ld_S2_))+S0.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S0 is not None) :
        features['d(ld(S2))p(S1)p(S0)='+str(state.tree.dtypes.get(ld_S2_))+S1.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S1 is not None) :
        features['d(ld(S2))p(S1)p(S1)='+str(state.tree.dtypes.get(ld_S2_))+S1.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S2 is not None) :
        features['d(ld(S2))p(S1)p(S2)='+str(state.tree.dtypes.get(ld_S2_))+S1.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S0 is not None) :
        features['d(ld(S2))p(S2)p(S0)='+str(state.tree.dtypes.get(ld_S2_))+S2.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S1 is not None) :
        features['d(ld(S2))p(S2)p(S1)='+str(state.tree.dtypes.get(ld_S2_))+S2.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S2 is not None) :
        features['d(ld(S2))p(S2)p(S2)='+str(state.tree.dtypes.get(ld_S2_))+S2.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S0 is not None) :
        features['d(rd(S0))p(S0)p(S0)='+str(state.tree.dtypes.get(rd_S0_))+S0.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S1 is not None) :
        features['d(rd(S0))p(S0)p(S1)='+str(state.tree.dtypes.get(rd_S0_))+S0.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S2 is not None) :
        features['d(rd(S0))p(S0)p(S2)='+str(state.tree.dtypes.get(rd_S0_))+S0.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S0 is not None) :
        features['d(rd(S0))p(S1)p(S0)='+str(state.tree.dtypes.get(rd_S0_))+S1.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S1 is not None) :
        features['d(rd(S0))p(S1)p(S1)='+str(state.tree.dtypes.get(rd_S0_))+S1.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S2 is not None) :
        features['d(rd(S0))p(S1)p(S2)='+str(state.tree.dtypes.get(rd_S0_))+S1.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S0 is not None) :
        features['d(rd(S0))p(S2)p(S0)='+str(state.tree.dtypes.get(rd_S0_))+S2.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S1 is not None) :
        features['d(rd(S0))p(S2)p(S1)='+str(state.tree.dtypes.get(rd_S0_))+S2.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S2 is not None) :
        features['d(rd(S0))p(S2)p(S2)='+str(state.tree.dtypes.get(rd_S0_))+S2.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S0 is not None) :
        features['d(rd(S1))p(S0)p(S0)='+str(state.tree.dtypes.get(rd_S1_))+S0.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S1 is not None) :
        features['d(rd(S1))p(S0)p(S1)='+str(state.tree.dtypes.get(rd_S1_))+S0.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S2 is not None) :
        features['d(rd(S1))p(S0)p(S2)='+str(state.tree.dtypes.get(rd_S1_))+S0.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S0 is not None) :
        features['d(rd(S1))p(S1)p(S0)='+str(state.tree.dtypes.get(rd_S1_))+S1.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S1 is not None) :
        features['d(rd(S1))p(S1)p(S1)='+str(state.tree.dtypes.get(rd_S1_))+S1.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S2 is not None) :
        features['d(rd(S1))p(S1)p(S2)='+str(state.tree.dtypes.get(rd_S1_))+S1.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S0 is not None) :
        features['d(rd(S1))p(S2)p(S0)='+str(state.tree.dtypes.get(rd_S1_))+S2.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S1 is not None) :
        features['d(rd(S1))p(S2)p(S1)='+str(state.tree.dtypes.get(rd_S1_))+S2.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S2 is not None) :
        features['d(rd(S1))p(S2)p(S2)='+str(state.tree.dtypes.get(rd_S1_))+S2.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S0 is not None) :
        features['d(rd(S2))p(S0)p(S0)='+str(state.tree.dtypes.get(rd_S2_))+S0.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S1 is not None) :
        features['d(rd(S2))p(S0)p(S1)='+str(state.tree.dtypes.get(rd_S2_))+S0.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S2 is not None) :
        features['d(rd(S2))p(S0)p(S2)='+str(state.tree.dtypes.get(rd_S2_))+S0.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S0 is not None) :
        features['d(rd(S2))p(S1)p(S0)='+str(state.tree.dtypes.get(rd_S2_))+S1.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S1 is not None) :
        features['d(rd(S2))p(S1)p(S1)='+str(state.tree.dtypes.get(rd_S2_))+S1.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S2 is not None) :
        features['d(rd(S2))p(S1)p(S2)='+str(state.tree.dtypes.get(rd_S2_))+S1.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S0 is not None) :
        features['d(rd(S2))p(S2)p(S0)='+str(state.tree.dtypes.get(rd_S2_))+S2.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S1 is not None) :
        features['d(rd(S2))p(S2)p(S1)='+str(state.tree.dtypes.get(rd_S2_))+S2.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S2 is not None) :
        features['d(rd(S2))p(S2)p(S2)='+str(state.tree.dtypes.get(rd_S2_))+S2.pos+S2.pos]=1.0
    if (S0 is not None) and (d0_S0_ is not None) and (d1_S0_ is not None) and (d2_S0_ is not None) :
        features['p(S0)d(d0(S0))d(d1(S0))d(d2(S0))='+S0.pos+str(state.tree.dtypes.get(d0_S0_))+str(state.tree.dtypes.get(d1_S0_))+str(state.tree.dtypes.get(d2_S0_))]=1.0
    if (S0 is not None) and (d0_S1_ is not None) and (d1_S1_ is not None) and (d2_S1_ is not None) :
        features['p(S0)d(d0(S1))d(d1(S1))d(d2(S1))='+S0.pos+str(state.tree.dtypes.get(d0_S1_))+str(state.tree.dtypes.get(d1_S1_))+str(state.tree.dtypes.get(d2_S1_))]=1.0
    if (S0 is not None) and (S0 is not None) and (d0_S0_ is not None) and (d1_S0_ is not None) and (d2_S0_ is not None) :
        features['p(S0)l(S0)d(d0(S0))d(d1(S0))d(d2(S0))='+S0.pos+S0.lemma+str(state.tree.dtypes.get(d0_S0_))+str(state.tree.dtypes.get(d1_S0_))+str(state.tree.dtypes.get(d2_S0_))]=1.0
    if (S0 is not None) and (S0 is not None) and (d0_S1_ is not None) and (d1_S1_ is not None) and (d2_S1_ is not None) :
        features['p(S0)l(S0)d(d0(S1))d(d1(S1))d(d2(S1))='+S0.pos+S0.lemma+str(state.tree.dtypes.get(d0_S1_))+str(state.tree.dtypes.get(d1_S1_))+str(state.tree.dtypes.get(d2_S1_))]=1.0
    return features
