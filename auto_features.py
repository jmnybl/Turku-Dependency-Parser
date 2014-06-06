
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




def get_following(token,idx,state):
    if token is None: return None
    if idx[0]==u"+":
        index=token.index+int(idx[1])
    elif idx[0]==u"-":
        index=token.index-int(idx[1])
    else: return None
    if index<0 or index>len(state.tree.tokens)-1: return None
    return state.tree.tokens[index]


def create_auto_features(state):
    S0,S1,S2=get_from_stack(state.stack)
    features={}
    d1_S0_=get_child(S0,'d1',state)
    rd_S0_=get_child(S0,'rd',state)
    d2_S0_=get_child(S0,'d2',state)
    ld_S2_=get_child(S2,'ld',state)
    ld_S0_=get_child(S0,'ld',state)
    Sleft20=get_following(S0,'-2',state)
    Sleft21=get_following(S1,'-2',state)
    d0_S1_=get_child(S1,'d0',state)
    Sright40=get_following(S0,'+4',state)
    Sright41=get_following(S1,'+4',state)
    Sright20=get_following(S0,'+2',state)
    Sright21=get_following(S1,'+2',state)
    d0_S0_=get_child(S0,'d0',state)
    Sleft11=get_following(S1,'-1',state)
    Sleft10=get_following(S0,'-1',state)
    d2_S1_=get_child(S1,'d2',state)
    Sleft31=get_following(S1,'-3',state)
    Sleft30=get_following(S0,'-3',state)
    d1_S1_=get_child(S1,'d1',state)
    ld_S1_=get_child(S1,'ld',state)
    Sright11=get_following(S1,'+1',state)
    Sright10=get_following(S0,'+1',state)
    rd_S1_=get_child(S1,'rd',state)
    Sright31=get_following(S1,'+3',state)
    Sright30=get_following(S0,'+3',state)
    if (S1 is not None) :
        features['p(S1)='+S1.pos]=1.0
    if (S0 is not None) :
        features['p(S0)='+S0.pos]=1.0
    if (S1 is not None) :
        features['l(S1)='+S1.lemma]=1.0
    if (S0 is not None) :
        features['l(S0)='+S0.lemma]=1.0
    if (S1 is not None) :
        features['w(S1)='+S1.text]=1.0
    if (S0 is not None) :
        features['w(S0)='+S0.text]=1.0
    if (Sright10 is not None) :
        features['p(S+10)='+Sright10.pos]=1.0
    if (Sright20 is not None) :
        features['p(S+20)='+Sright20.pos]=1.0
    if (ld_S0_ is not None) :
        features['w(ld(S0))='+ld_S0_.text]=1.0
    if (ld_S1_ is not None) :
        features['w(ld(S1))='+ld_S1_.text]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['w(S1)p(S0)='+S1.text+S0.pos]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['p(S1)w(S0)='+S1.pos+S0.text]=1.0
    if (S0 is not None) and (S0 is not None) :
        features['w(S0)p(S0)='+S0.text+S0.pos]=1.0
    if (S1 is not None) and (S1 is not None) :
        features['w(S1)p(S1)='+S1.text+S1.pos]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['w(S1)w(S0)='+S1.text+S0.text]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['l(S1)p(S0)='+S1.lemma+S0.pos]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['p(S1)l(S0)='+S1.pos+S0.lemma]=1.0
    if (Sright20 is not None) and (Sright20 is not None) :
        features['w(S+20)p(S+20)='+Sright20.text+Sright20.pos]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['p(S1)p(S0)='+S1.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) :
        features['w(S+10)p(S+10)='+Sright10.text+Sright10.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+11)w(S+20)p(S0)='+Sright11.text+Sright20.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+21)w(S+30)p(S0)='+Sright21.text+Sright30.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+21)w(S+10)p(S1)='+Sright21.text+Sright10.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+31)w(S+20)p(S1)='+Sright31.text+Sright20.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['p(S+11)w(S+20)p(S0)='+Sright11.pos+Sright20.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['p(S+21)w(S+30)p(S0)='+Sright21.pos+Sright30.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+10)p(S+21)p(S0)='+Sright10.text+Sright21.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+20)p(S+31)p(S0)='+Sright20.text+Sright31.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+11)w(S+21)p(S0)='+Sright11.text+Sright21.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+21)w(S+31)p(S0)='+Sright21.text+Sright31.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+31)w(S+41)p(S0)='+Sright31.text+Sright41.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+10)w(S+20)p(S1)='+Sright10.text+Sright20.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+20)w(S+30)p(S1)='+Sright20.text+Sright30.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+30)w(S+40)p(S1)='+Sright30.text+Sright40.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sleft11 is not None) and (S0 is not None) :
        features['w(S+21)w(S-11)p(S0)='+Sright21.text+Sleft11.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sleft11 is not None) and (S0 is not None) :
        features['w(S+31)w(S-11)p(S0)='+Sright31.text+Sleft11.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sleft10 is not None) and (S1 is not None) :
        features['w(S+20)w(S-10)p(S1)='+Sright20.text+Sleft10.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sleft10 is not None) and (S1 is not None) :
        features['w(S+30)w(S-10)p(S1)='+Sright30.text+Sleft10.text+S1.pos]=1.0
    if (Sleft11 is not None) and (Sleft21 is not None) and (S0 is not None) :
        features['w(S-11)w(S-21)p(S0)='+Sleft11.text+Sleft21.text+S0.pos]=1.0
    if (Sleft21 is not None) and (Sleft31 is not None) and (S1 is not None) :
        features['w(S-21)w(S-31)p(S1)='+Sleft21.text+Sleft31.text+S1.pos]=1.0
    if (Sleft10 is not None) and (Sleft20 is not None) and (S1 is not None) :
        features['w(S-10)w(S-20)p(S1)='+Sleft10.text+Sleft20.text+S1.pos]=1.0
    if (Sleft20 is not None) and (Sleft30 is not None) and (S1 is not None) :
        features['w(S-20)w(S-30)p(S1)='+Sleft20.text+Sleft30.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['p(S+11)p(S+21)p(S0)='+Sright11.pos+Sright21.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['p(S+21)p(S+31)p(S0)='+Sright21.pos+Sright31.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['p(S+31)p(S+41)p(S0)='+Sright31.pos+Sright41.pos+S0.pos]=1.0
    if (Sleft11 is not None) and (Sleft21 is not None) and (S0 is not None) :
        features['p(S-11)p(S-21)p(S0)='+Sleft11.pos+Sleft21.pos+S0.pos]=1.0
    if (Sleft21 is not None) and (Sleft31 is not None) and (S0 is not None) :
        features['p(S-21)p(S-31)p(S0)='+Sleft21.pos+Sleft31.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['p(S+10)p(S+20)p(S1)='+Sright10.pos+Sright20.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['p(S+20)p(S+30)p(S1)='+Sright20.pos+Sright30.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['p(S+30)p(S+40)p(S1)='+Sright30.pos+Sright40.pos+S1.pos]=1.0
    if (Sleft10 is not None) and (Sleft20 is not None) and (S1 is not None) :
        features['p(S-10)p(S-20)p(S1)='+Sleft10.pos+Sleft20.pos+S1.pos]=1.0
    if (Sleft20 is not None) and (Sleft30 is not None) and (S1 is not None) :
        features['p(S-20)p(S-30)p(S1)='+Sleft20.pos+Sleft30.pos+S1.pos]=1.0
    if (S0 is not None) and (S1 is not None) and (rd_S1_ is not None) :
        features['w(S0)p(S1)w(rd(S1))='+S0.text+S1.pos+rd_S1_.text]=1.0
    if (S1 is not None) and (S0 is not None) and (rd_S1_ is not None) :
        features['w(S1)p(S0)w(rd(S1))='+S1.text+S0.pos+rd_S1_.text]=1.0
    if (S0 is not None) and (S1 is not None) and (rd_S1_ is not None) :
        features['l(S0)p(S1)l(rd(S1))='+S0.lemma+S1.pos+rd_S1_.lemma]=1.0
    if (S1 is not None) and (S0 is not None) and (rd_S1_ is not None) :
        features['l(S1)p(S0)l(rd(S1))='+S1.lemma+S0.pos+rd_S1_.lemma]=1.0
    if (S0 is not None) and (d0_S1_ is not None) and (d1_S1_ is not None) :
        features['p(S0)p(d0(S1))w(d1(S1))='+S0.pos+d0_S1_.pos+d1_S1_.text]=1.0
    if (S0 is not None) and (d0_S1_ is not None) and (d1_S1_ is not None) :
        features['p(S0)p(d0(S1))p(d1(S1))='+S0.pos+d0_S1_.pos+d1_S1_.pos]=1.0
    if (S0 is not None) and (S1 is not None) and (ld_S2_ is not None) :
        features['p(S0)p(S1)p(ld(S2))='+S0.pos+S1.pos+ld_S2_.pos]=1.0
    if (S0 is not None) and (S1 is not None) and (S2 is not None) :
        features['p(S0)p(S1)p(S2)='+S0.pos+S1.pos+S2.pos]=1.0
    if (S0 is not None) and (S0 is not None) and (rd_S0_ is not None) :
        features['w(S0)p(S0)p(rd(S0))='+S0.text+S0.pos+rd_S0_.pos]=1.0
    if (S0 is not None) and (d0_S0_ is not None) and (d1_S0_ is not None) :
        features['p(S0)p(d0(S0))p(d1(S0))='+S0.pos+d0_S0_.pos+d1_S0_.pos]=1.0
    if (S0 is not None) and (Sright10 is not None) and (S1 is not None) and (S0 is not None) :
        features['w(S0)w(S+10)p(S1)p(S0)='+S0.text+Sright10.text+S1.pos+S0.pos]=1.0
    if (S0 is not None) and (d0_S0_ is not None) and (d1_S0_ is not None) and (d2_S0_ is not None) :
        features['p(S0)p(d0(S0))p(d1(S0))p(d2(S0))='+S0.pos+d0_S0_.pos+d1_S0_.pos+d2_S0_.pos]=1.0
    if (S0 is not None) and (d0_S1_ is not None) and (d1_S1_ is not None) and (d2_S1_ is not None) :
        features['p(S0)p(d0(S1))p(d1(S1))p(d2(S1))='+S0.pos+d0_S1_.pos+d1_S1_.pos+d2_S1_.pos]=1.0
    return features
