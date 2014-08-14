
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



def get_from_queue(queue):
    r=[None,None,None,None,None]
    for i,qi in enumerate(queue[:5]):
         r[i]=qi
    return tuple(r)



def create_auto_features(state):
    S0,S1,S2=get_from_stack(state.stack)
    B0,B1,B2,B3,B4=get_from_queue(state.queue)
    features={}
    d1_S0_=get_child(S0,'d1',state)
    rd_S0_=get_child(S0,'rd',state)
    d2_S0_=get_child(S0,'d2',state)
    ld_S2_=get_child(S2,'ld',state)
    ld_S0_=get_child(S0,'ld',state)
    d0_S1_=get_child(S1,'d0',state)
    Sright42=get_following(S2,'+4',state)
    Sright40=get_following(S0,'+4',state)
    Sright41=get_following(S1,'+4',state)
    rd_S2_=get_child(S2,'rd',state)
    Sright20=get_following(S0,'+2',state)
    Sright21=get_following(S1,'+2',state)
    Sright22=get_following(S2,'+2',state)
    d0_S0_=get_child(S0,'d0',state)
    d2_S1_=get_child(S1,'d2',state)
    d1_S1_=get_child(S1,'d1',state)
    ld_S1_=get_child(S1,'ld',state)
    Sright11=get_following(S1,'+1',state)
    Sright10=get_following(S0,'+1',state)
    Sright12=get_following(S2,'+1',state)
    rd_S1_=get_child(S1,'rd',state)
    Sright32=get_following(S2,'+3',state)
    Sright31=get_following(S1,'+3',state)
    Sright30=get_following(S0,'+3',state)
    if (B0 is not None) and (S0 is not None) :
        features['l(B0)l(S0)='+B0.lemma+S0.lemma]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['l(B0)l(S1)='+B0.lemma+S1.lemma]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['l(B0)l(S2)='+B0.lemma+S2.lemma]=1.0
    if (B0 is not None) and (B0 is not None) :
        features['l(B0)p(B0)='+B0.lemma+B0.pos]=1.0
    if (B0 is not None) and (B1 is not None) :
        features['l(B0)p(B1)='+B0.lemma+B1.pos]=1.0
    if (B0 is not None) and (B2 is not None) :
        features['l(B0)p(B2)='+B0.lemma+B2.pos]=1.0
    if (B0 is not None) and (B3 is not None) :
        features['l(B0)p(B3)='+B0.lemma+B3.pos]=1.0
    if (B0 is not None) and (B4 is not None) :
        features['l(B0)p(B4)='+B0.lemma+B4.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['l(B0)p(S0)='+B0.lemma+S0.pos]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['l(B0)p(S1)='+B0.lemma+S1.pos]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['l(B0)p(S2)='+B0.lemma+S2.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['l(B0)w(S0)='+B0.lemma+S0.text]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['l(B0)w(S1)='+B0.lemma+S1.text]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['l(B0)w(S2)='+B0.lemma+S2.text]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['l(B1)l(S0)='+B1.lemma+S0.lemma]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['l(B1)l(S1)='+B1.lemma+S1.lemma]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['l(B1)l(S2)='+B1.lemma+S2.lemma]=1.0
    if (B1 is not None) and (B0 is not None) :
        features['l(B1)p(B0)='+B1.lemma+B0.pos]=1.0
    if (B1 is not None) and (B1 is not None) :
        features['l(B1)p(B1)='+B1.lemma+B1.pos]=1.0
    if (B1 is not None) and (B2 is not None) :
        features['l(B1)p(B2)='+B1.lemma+B2.pos]=1.0
    if (B1 is not None) and (B3 is not None) :
        features['l(B1)p(B3)='+B1.lemma+B3.pos]=1.0
    if (B1 is not None) and (B4 is not None) :
        features['l(B1)p(B4)='+B1.lemma+B4.pos]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['l(B1)p(S0)='+B1.lemma+S0.pos]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['l(B1)p(S1)='+B1.lemma+S1.pos]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['l(B1)p(S2)='+B1.lemma+S2.pos]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['l(B1)w(S0)='+B1.lemma+S0.text]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['l(B1)w(S1)='+B1.lemma+S1.text]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['l(B1)w(S2)='+B1.lemma+S2.text]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['l(B2)l(S0)='+B2.lemma+S0.lemma]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['l(B2)l(S1)='+B2.lemma+S1.lemma]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['l(B2)l(S2)='+B2.lemma+S2.lemma]=1.0
    if (B2 is not None) and (B0 is not None) :
        features['l(B2)p(B0)='+B2.lemma+B0.pos]=1.0
    if (B2 is not None) and (B1 is not None) :
        features['l(B2)p(B1)='+B2.lemma+B1.pos]=1.0
    if (B2 is not None) and (B2 is not None) :
        features['l(B2)p(B2)='+B2.lemma+B2.pos]=1.0
    if (B2 is not None) and (B3 is not None) :
        features['l(B2)p(B3)='+B2.lemma+B3.pos]=1.0
    if (B2 is not None) and (B4 is not None) :
        features['l(B2)p(B4)='+B2.lemma+B4.pos]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['l(B2)p(S0)='+B2.lemma+S0.pos]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['l(B2)p(S1)='+B2.lemma+S1.pos]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['l(B2)p(S2)='+B2.lemma+S2.pos]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['l(B2)w(S0)='+B2.lemma+S0.text]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['l(B2)w(S1)='+B2.lemma+S1.text]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['l(B2)w(S2)='+B2.lemma+S2.text]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['l(B3)l(S0)='+B3.lemma+S0.lemma]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['l(B3)l(S1)='+B3.lemma+S1.lemma]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['l(B3)l(S2)='+B3.lemma+S2.lemma]=1.0
    if (B3 is not None) and (B0 is not None) :
        features['l(B3)p(B0)='+B3.lemma+B0.pos]=1.0
    if (B3 is not None) and (B1 is not None) :
        features['l(B3)p(B1)='+B3.lemma+B1.pos]=1.0
    if (B3 is not None) and (B2 is not None) :
        features['l(B3)p(B2)='+B3.lemma+B2.pos]=1.0
    if (B3 is not None) and (B3 is not None) :
        features['l(B3)p(B3)='+B3.lemma+B3.pos]=1.0
    if (B3 is not None) and (B4 is not None) :
        features['l(B3)p(B4)='+B3.lemma+B4.pos]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['l(B3)p(S0)='+B3.lemma+S0.pos]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['l(B3)p(S1)='+B3.lemma+S1.pos]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['l(B3)p(S2)='+B3.lemma+S2.pos]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['l(B3)w(S0)='+B3.lemma+S0.text]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['l(B3)w(S1)='+B3.lemma+S1.text]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['l(B3)w(S2)='+B3.lemma+S2.text]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['l(B4)l(S0)='+B4.lemma+S0.lemma]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['l(B4)l(S1)='+B4.lemma+S1.lemma]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['l(B4)l(S2)='+B4.lemma+S2.lemma]=1.0
    if (B4 is not None) and (B0 is not None) :
        features['l(B4)p(B0)='+B4.lemma+B0.pos]=1.0
    if (B4 is not None) and (B1 is not None) :
        features['l(B4)p(B1)='+B4.lemma+B1.pos]=1.0
    if (B4 is not None) and (B2 is not None) :
        features['l(B4)p(B2)='+B4.lemma+B2.pos]=1.0
    if (B4 is not None) and (B3 is not None) :
        features['l(B4)p(B3)='+B4.lemma+B3.pos]=1.0
    if (B4 is not None) and (B4 is not None) :
        features['l(B4)p(B4)='+B4.lemma+B4.pos]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['l(B4)p(S0)='+B4.lemma+S0.pos]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['l(B4)p(S1)='+B4.lemma+S1.pos]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['l(B4)p(S2)='+B4.lemma+S2.pos]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['l(B4)w(S0)='+B4.lemma+S0.text]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['l(B4)w(S1)='+B4.lemma+S1.text]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['l(B4)w(S2)='+B4.lemma+S2.text]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+10)l(S+10)p(S0)='+Sright10.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+10)l(S+10)p(S1)='+Sright10.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+10)l(S+10)p(S2)='+Sright10.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+10)l(S+11)p(S0)='+Sright10.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+10)l(S+11)p(S1)='+Sright10.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+10)l(S+11)p(S2)='+Sright10.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+10)l(S+12)p(S0)='+Sright10.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+10)l(S+12)p(S1)='+Sright10.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+10)l(S+12)p(S2)='+Sright10.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+10)l(S+20)p(S0)='+Sright10.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+10)l(S+20)p(S1)='+Sright10.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+10)l(S+20)p(S2)='+Sright10.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+10)l(S+21)p(S0)='+Sright10.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+10)l(S+21)p(S1)='+Sright10.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+10)l(S+21)p(S2)='+Sright10.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+10)l(S+22)p(S0)='+Sright10.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+10)l(S+22)p(S1)='+Sright10.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+10)l(S+22)p(S2)='+Sright10.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+10)l(S+30)p(S0)='+Sright10.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+10)l(S+30)p(S1)='+Sright10.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+10)l(S+30)p(S2)='+Sright10.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+10)l(S+31)p(S0)='+Sright10.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+10)l(S+31)p(S1)='+Sright10.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+10)l(S+31)p(S2)='+Sright10.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+10)l(S+32)p(S0)='+Sright10.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+10)l(S+32)p(S1)='+Sright10.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+10)l(S+32)p(S2)='+Sright10.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+10)l(S+40)p(S0)='+Sright10.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+10)l(S+40)p(S1)='+Sright10.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+10)l(S+40)p(S2)='+Sright10.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+10)l(S+41)p(S0)='+Sright10.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+10)l(S+41)p(S1)='+Sright10.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+10)l(S+41)p(S2)='+Sright10.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+10)l(S+42)p(S0)='+Sright10.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+10)l(S+42)p(S1)='+Sright10.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+10)l(S+42)p(S2)='+Sright10.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+10)p(S+10)p(S0)='+Sright10.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+10)p(S+10)p(S1)='+Sright10.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+10)p(S+10)p(S2)='+Sright10.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+10)p(S+11)p(S0)='+Sright10.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+10)p(S+11)p(S1)='+Sright10.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+10)p(S+11)p(S2)='+Sright10.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+10)p(S+12)p(S0)='+Sright10.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+10)p(S+12)p(S1)='+Sright10.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+10)p(S+12)p(S2)='+Sright10.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+10)p(S+20)p(S0)='+Sright10.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+10)p(S+20)p(S1)='+Sright10.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+10)p(S+20)p(S2)='+Sright10.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+10)p(S+21)p(S0)='+Sright10.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+10)p(S+21)p(S1)='+Sright10.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+10)p(S+21)p(S2)='+Sright10.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+10)p(S+22)p(S0)='+Sright10.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+10)p(S+22)p(S1)='+Sright10.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+10)p(S+22)p(S2)='+Sright10.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+10)p(S+30)p(S0)='+Sright10.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+10)p(S+30)p(S1)='+Sright10.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+10)p(S+30)p(S2)='+Sright10.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+10)p(S+31)p(S0)='+Sright10.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+10)p(S+31)p(S1)='+Sright10.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+10)p(S+31)p(S2)='+Sright10.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+10)p(S+32)p(S0)='+Sright10.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+10)p(S+32)p(S1)='+Sright10.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+10)p(S+32)p(S2)='+Sright10.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+10)p(S+40)p(S0)='+Sright10.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+10)p(S+40)p(S1)='+Sright10.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+10)p(S+40)p(S2)='+Sright10.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+10)p(S+41)p(S0)='+Sright10.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+10)p(S+41)p(S1)='+Sright10.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+10)p(S+41)p(S2)='+Sright10.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+10)p(S+42)p(S0)='+Sright10.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+10)p(S+42)p(S1)='+Sright10.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+10)p(S+42)p(S2)='+Sright10.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+10)w(S+10)p(S0)='+Sright10.lemma+Sright10.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+10)w(S+10)p(S1)='+Sright10.lemma+Sright10.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+10)w(S+10)p(S2)='+Sright10.lemma+Sright10.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+10)w(S+11)p(S0)='+Sright10.lemma+Sright11.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+10)w(S+11)p(S1)='+Sright10.lemma+Sright11.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+10)w(S+11)p(S2)='+Sright10.lemma+Sright11.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+10)w(S+12)p(S0)='+Sright10.lemma+Sright12.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+10)w(S+12)p(S1)='+Sright10.lemma+Sright12.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+10)w(S+12)p(S2)='+Sright10.lemma+Sright12.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+10)w(S+20)p(S0)='+Sright10.lemma+Sright20.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+10)w(S+20)p(S1)='+Sright10.lemma+Sright20.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+10)w(S+20)p(S2)='+Sright10.lemma+Sright20.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+10)w(S+21)p(S0)='+Sright10.lemma+Sright21.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+10)w(S+21)p(S1)='+Sright10.lemma+Sright21.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+10)w(S+21)p(S2)='+Sright10.lemma+Sright21.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+10)w(S+22)p(S0)='+Sright10.lemma+Sright22.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+10)w(S+22)p(S1)='+Sright10.lemma+Sright22.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+10)w(S+22)p(S2)='+Sright10.lemma+Sright22.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+10)w(S+30)p(S0)='+Sright10.lemma+Sright30.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+10)w(S+30)p(S1)='+Sright10.lemma+Sright30.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+10)w(S+30)p(S2)='+Sright10.lemma+Sright30.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+10)w(S+31)p(S0)='+Sright10.lemma+Sright31.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+10)w(S+31)p(S1)='+Sright10.lemma+Sright31.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+10)w(S+31)p(S2)='+Sright10.lemma+Sright31.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+10)w(S+32)p(S0)='+Sright10.lemma+Sright32.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+10)w(S+32)p(S1)='+Sright10.lemma+Sright32.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+10)w(S+32)p(S2)='+Sright10.lemma+Sright32.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+10)w(S+40)p(S0)='+Sright10.lemma+Sright40.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+10)w(S+40)p(S1)='+Sright10.lemma+Sright40.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+10)w(S+40)p(S2)='+Sright10.lemma+Sright40.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+10)w(S+41)p(S0)='+Sright10.lemma+Sright41.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+10)w(S+41)p(S1)='+Sright10.lemma+Sright41.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+10)w(S+41)p(S2)='+Sright10.lemma+Sright41.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+10)w(S+42)p(S0)='+Sright10.lemma+Sright42.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+10)w(S+42)p(S1)='+Sright10.lemma+Sright42.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+10)w(S+42)p(S2)='+Sright10.lemma+Sright42.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+11)l(S+10)p(S0)='+Sright11.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+11)l(S+10)p(S1)='+Sright11.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+11)l(S+10)p(S2)='+Sright11.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+11)l(S+11)p(S0)='+Sright11.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+11)l(S+11)p(S1)='+Sright11.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+11)l(S+11)p(S2)='+Sright11.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+11)l(S+12)p(S0)='+Sright11.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+11)l(S+12)p(S1)='+Sright11.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+11)l(S+12)p(S2)='+Sright11.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+11)l(S+20)p(S0)='+Sright11.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+11)l(S+20)p(S1)='+Sright11.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+11)l(S+20)p(S2)='+Sright11.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+11)l(S+21)p(S0)='+Sright11.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+11)l(S+21)p(S1)='+Sright11.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+11)l(S+21)p(S2)='+Sright11.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+11)l(S+22)p(S0)='+Sright11.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+11)l(S+22)p(S1)='+Sright11.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+11)l(S+22)p(S2)='+Sright11.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+11)l(S+30)p(S0)='+Sright11.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+11)l(S+30)p(S1)='+Sright11.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+11)l(S+30)p(S2)='+Sright11.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+11)l(S+31)p(S0)='+Sright11.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+11)l(S+31)p(S1)='+Sright11.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+11)l(S+31)p(S2)='+Sright11.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+11)l(S+32)p(S0)='+Sright11.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+11)l(S+32)p(S1)='+Sright11.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+11)l(S+32)p(S2)='+Sright11.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+11)l(S+40)p(S0)='+Sright11.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+11)l(S+40)p(S1)='+Sright11.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+11)l(S+40)p(S2)='+Sright11.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+11)l(S+41)p(S0)='+Sright11.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+11)l(S+41)p(S1)='+Sright11.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+11)l(S+41)p(S2)='+Sright11.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+11)l(S+42)p(S0)='+Sright11.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+11)l(S+42)p(S1)='+Sright11.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+11)l(S+42)p(S2)='+Sright11.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+11)p(S+10)p(S0)='+Sright11.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+11)p(S+10)p(S1)='+Sright11.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+11)p(S+10)p(S2)='+Sright11.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+11)p(S+11)p(S0)='+Sright11.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+11)p(S+11)p(S1)='+Sright11.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+11)p(S+11)p(S2)='+Sright11.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+11)p(S+12)p(S0)='+Sright11.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+11)p(S+12)p(S1)='+Sright11.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+11)p(S+12)p(S2)='+Sright11.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+11)p(S+20)p(S0)='+Sright11.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+11)p(S+20)p(S1)='+Sright11.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+11)p(S+20)p(S2)='+Sright11.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+11)p(S+21)p(S0)='+Sright11.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+11)p(S+21)p(S1)='+Sright11.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+11)p(S+21)p(S2)='+Sright11.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+11)p(S+22)p(S0)='+Sright11.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+11)p(S+22)p(S1)='+Sright11.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+11)p(S+22)p(S2)='+Sright11.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+11)p(S+30)p(S0)='+Sright11.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+11)p(S+30)p(S1)='+Sright11.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+11)p(S+30)p(S2)='+Sright11.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+11)p(S+31)p(S0)='+Sright11.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+11)p(S+31)p(S1)='+Sright11.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+11)p(S+31)p(S2)='+Sright11.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+11)p(S+32)p(S0)='+Sright11.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+11)p(S+32)p(S1)='+Sright11.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+11)p(S+32)p(S2)='+Sright11.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+11)p(S+40)p(S0)='+Sright11.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+11)p(S+40)p(S1)='+Sright11.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+11)p(S+40)p(S2)='+Sright11.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+11)p(S+41)p(S0)='+Sright11.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+11)p(S+41)p(S1)='+Sright11.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+11)p(S+41)p(S2)='+Sright11.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+11)p(S+42)p(S0)='+Sright11.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+11)p(S+42)p(S1)='+Sright11.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+11)p(S+42)p(S2)='+Sright11.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+11)w(S+10)p(S0)='+Sright11.lemma+Sright10.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+11)w(S+10)p(S1)='+Sright11.lemma+Sright10.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+11)w(S+10)p(S2)='+Sright11.lemma+Sright10.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+11)w(S+11)p(S0)='+Sright11.lemma+Sright11.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+11)w(S+11)p(S1)='+Sright11.lemma+Sright11.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+11)w(S+11)p(S2)='+Sright11.lemma+Sright11.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+11)w(S+12)p(S0)='+Sright11.lemma+Sright12.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+11)w(S+12)p(S1)='+Sright11.lemma+Sright12.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+11)w(S+12)p(S2)='+Sright11.lemma+Sright12.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+11)w(S+20)p(S0)='+Sright11.lemma+Sright20.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+11)w(S+20)p(S1)='+Sright11.lemma+Sright20.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+11)w(S+20)p(S2)='+Sright11.lemma+Sright20.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+11)w(S+21)p(S0)='+Sright11.lemma+Sright21.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+11)w(S+21)p(S1)='+Sright11.lemma+Sright21.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+11)w(S+21)p(S2)='+Sright11.lemma+Sright21.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+11)w(S+22)p(S0)='+Sright11.lemma+Sright22.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+11)w(S+22)p(S1)='+Sright11.lemma+Sright22.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+11)w(S+22)p(S2)='+Sright11.lemma+Sright22.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+11)w(S+30)p(S0)='+Sright11.lemma+Sright30.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+11)w(S+30)p(S1)='+Sright11.lemma+Sright30.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+11)w(S+30)p(S2)='+Sright11.lemma+Sright30.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+11)w(S+31)p(S0)='+Sright11.lemma+Sright31.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+11)w(S+31)p(S1)='+Sright11.lemma+Sright31.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+11)w(S+31)p(S2)='+Sright11.lemma+Sright31.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+11)w(S+32)p(S0)='+Sright11.lemma+Sright32.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+11)w(S+32)p(S1)='+Sright11.lemma+Sright32.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+11)w(S+32)p(S2)='+Sright11.lemma+Sright32.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+11)w(S+40)p(S0)='+Sright11.lemma+Sright40.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+11)w(S+40)p(S1)='+Sright11.lemma+Sright40.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+11)w(S+40)p(S2)='+Sright11.lemma+Sright40.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+11)w(S+41)p(S0)='+Sright11.lemma+Sright41.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+11)w(S+41)p(S1)='+Sright11.lemma+Sright41.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+11)w(S+41)p(S2)='+Sright11.lemma+Sright41.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+11)w(S+42)p(S0)='+Sright11.lemma+Sright42.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+11)w(S+42)p(S1)='+Sright11.lemma+Sright42.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+11)w(S+42)p(S2)='+Sright11.lemma+Sright42.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+12)l(S+10)p(S0)='+Sright12.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+12)l(S+10)p(S1)='+Sright12.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+12)l(S+10)p(S2)='+Sright12.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+12)l(S+11)p(S0)='+Sright12.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+12)l(S+11)p(S1)='+Sright12.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+12)l(S+11)p(S2)='+Sright12.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+12)l(S+12)p(S0)='+Sright12.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+12)l(S+12)p(S1)='+Sright12.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+12)l(S+12)p(S2)='+Sright12.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+12)l(S+20)p(S0)='+Sright12.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+12)l(S+20)p(S1)='+Sright12.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+12)l(S+20)p(S2)='+Sright12.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+12)l(S+21)p(S0)='+Sright12.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+12)l(S+21)p(S1)='+Sright12.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+12)l(S+21)p(S2)='+Sright12.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+12)l(S+22)p(S0)='+Sright12.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+12)l(S+22)p(S1)='+Sright12.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+12)l(S+22)p(S2)='+Sright12.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+12)l(S+30)p(S0)='+Sright12.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+12)l(S+30)p(S1)='+Sright12.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+12)l(S+30)p(S2)='+Sright12.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+12)l(S+31)p(S0)='+Sright12.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+12)l(S+31)p(S1)='+Sright12.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+12)l(S+31)p(S2)='+Sright12.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+12)l(S+32)p(S0)='+Sright12.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+12)l(S+32)p(S1)='+Sright12.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+12)l(S+32)p(S2)='+Sright12.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+12)l(S+40)p(S0)='+Sright12.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+12)l(S+40)p(S1)='+Sright12.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+12)l(S+40)p(S2)='+Sright12.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+12)l(S+41)p(S0)='+Sright12.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+12)l(S+41)p(S1)='+Sright12.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+12)l(S+41)p(S2)='+Sright12.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+12)l(S+42)p(S0)='+Sright12.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+12)l(S+42)p(S1)='+Sright12.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+12)l(S+42)p(S2)='+Sright12.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+12)p(S+10)p(S0)='+Sright12.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+12)p(S+10)p(S1)='+Sright12.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+12)p(S+10)p(S2)='+Sright12.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+12)p(S+11)p(S0)='+Sright12.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+12)p(S+11)p(S1)='+Sright12.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+12)p(S+11)p(S2)='+Sright12.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+12)p(S+12)p(S0)='+Sright12.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+12)p(S+12)p(S1)='+Sright12.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+12)p(S+12)p(S2)='+Sright12.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+12)p(S+20)p(S0)='+Sright12.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+12)p(S+20)p(S1)='+Sright12.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+12)p(S+20)p(S2)='+Sright12.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+12)p(S+21)p(S0)='+Sright12.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+12)p(S+21)p(S1)='+Sright12.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+12)p(S+21)p(S2)='+Sright12.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+12)p(S+22)p(S0)='+Sright12.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+12)p(S+22)p(S1)='+Sright12.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+12)p(S+22)p(S2)='+Sright12.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+12)p(S+30)p(S0)='+Sright12.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+12)p(S+30)p(S1)='+Sright12.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+12)p(S+30)p(S2)='+Sright12.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+12)p(S+31)p(S0)='+Sright12.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+12)p(S+31)p(S1)='+Sright12.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+12)p(S+31)p(S2)='+Sright12.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+12)p(S+32)p(S0)='+Sright12.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+12)p(S+32)p(S1)='+Sright12.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+12)p(S+32)p(S2)='+Sright12.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+12)p(S+40)p(S0)='+Sright12.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+12)p(S+40)p(S1)='+Sright12.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+12)p(S+40)p(S2)='+Sright12.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+12)p(S+41)p(S0)='+Sright12.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+12)p(S+41)p(S1)='+Sright12.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+12)p(S+41)p(S2)='+Sright12.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+12)p(S+42)p(S0)='+Sright12.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+12)p(S+42)p(S1)='+Sright12.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+12)p(S+42)p(S2)='+Sright12.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+12)w(S+10)p(S0)='+Sright12.lemma+Sright10.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+12)w(S+10)p(S1)='+Sright12.lemma+Sright10.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+12)w(S+10)p(S2)='+Sright12.lemma+Sright10.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+12)w(S+11)p(S0)='+Sright12.lemma+Sright11.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+12)w(S+11)p(S1)='+Sright12.lemma+Sright11.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+12)w(S+11)p(S2)='+Sright12.lemma+Sright11.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+12)w(S+12)p(S0)='+Sright12.lemma+Sright12.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+12)w(S+12)p(S1)='+Sright12.lemma+Sright12.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+12)w(S+12)p(S2)='+Sright12.lemma+Sright12.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+12)w(S+20)p(S0)='+Sright12.lemma+Sright20.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+12)w(S+20)p(S1)='+Sright12.lemma+Sright20.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+12)w(S+20)p(S2)='+Sright12.lemma+Sright20.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+12)w(S+21)p(S0)='+Sright12.lemma+Sright21.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+12)w(S+21)p(S1)='+Sright12.lemma+Sright21.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+12)w(S+21)p(S2)='+Sright12.lemma+Sright21.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+12)w(S+22)p(S0)='+Sright12.lemma+Sright22.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+12)w(S+22)p(S1)='+Sright12.lemma+Sright22.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+12)w(S+22)p(S2)='+Sright12.lemma+Sright22.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+12)w(S+30)p(S0)='+Sright12.lemma+Sright30.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+12)w(S+30)p(S1)='+Sright12.lemma+Sright30.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+12)w(S+30)p(S2)='+Sright12.lemma+Sright30.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+12)w(S+31)p(S0)='+Sright12.lemma+Sright31.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+12)w(S+31)p(S1)='+Sright12.lemma+Sright31.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+12)w(S+31)p(S2)='+Sright12.lemma+Sright31.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+12)w(S+32)p(S0)='+Sright12.lemma+Sright32.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+12)w(S+32)p(S1)='+Sright12.lemma+Sright32.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+12)w(S+32)p(S2)='+Sright12.lemma+Sright32.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+12)w(S+40)p(S0)='+Sright12.lemma+Sright40.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+12)w(S+40)p(S1)='+Sright12.lemma+Sright40.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+12)w(S+40)p(S2)='+Sright12.lemma+Sright40.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+12)w(S+41)p(S0)='+Sright12.lemma+Sright41.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+12)w(S+41)p(S1)='+Sright12.lemma+Sright41.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+12)w(S+41)p(S2)='+Sright12.lemma+Sright41.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+12)w(S+42)p(S0)='+Sright12.lemma+Sright42.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+12)w(S+42)p(S1)='+Sright12.lemma+Sright42.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+12)w(S+42)p(S2)='+Sright12.lemma+Sright42.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+20)l(S+10)p(S0)='+Sright20.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+20)l(S+10)p(S1)='+Sright20.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+20)l(S+10)p(S2)='+Sright20.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+20)l(S+11)p(S0)='+Sright20.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+20)l(S+11)p(S1)='+Sright20.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+20)l(S+11)p(S2)='+Sright20.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+20)l(S+12)p(S0)='+Sright20.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+20)l(S+12)p(S1)='+Sright20.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+20)l(S+12)p(S2)='+Sright20.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+20)l(S+20)p(S0)='+Sright20.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+20)l(S+20)p(S1)='+Sright20.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+20)l(S+20)p(S2)='+Sright20.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+20)l(S+21)p(S0)='+Sright20.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+20)l(S+21)p(S1)='+Sright20.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+20)l(S+21)p(S2)='+Sright20.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+20)l(S+22)p(S0)='+Sright20.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+20)l(S+22)p(S1)='+Sright20.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+20)l(S+22)p(S2)='+Sright20.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+20)l(S+30)p(S0)='+Sright20.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+20)l(S+30)p(S1)='+Sright20.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+20)l(S+30)p(S2)='+Sright20.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+20)l(S+31)p(S0)='+Sright20.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+20)l(S+31)p(S1)='+Sright20.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+20)l(S+31)p(S2)='+Sright20.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+20)l(S+32)p(S0)='+Sright20.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+20)l(S+32)p(S1)='+Sright20.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+20)l(S+32)p(S2)='+Sright20.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+20)l(S+40)p(S0)='+Sright20.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+20)l(S+40)p(S1)='+Sright20.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+20)l(S+40)p(S2)='+Sright20.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+20)l(S+41)p(S0)='+Sright20.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+20)l(S+41)p(S1)='+Sright20.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+20)l(S+41)p(S2)='+Sright20.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+20)l(S+42)p(S0)='+Sright20.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+20)l(S+42)p(S1)='+Sright20.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+20)l(S+42)p(S2)='+Sright20.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+20)p(S+10)p(S0)='+Sright20.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+20)p(S+10)p(S1)='+Sright20.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+20)p(S+10)p(S2)='+Sright20.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+20)p(S+11)p(S0)='+Sright20.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+20)p(S+11)p(S1)='+Sright20.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+20)p(S+11)p(S2)='+Sright20.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+20)p(S+12)p(S0)='+Sright20.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+20)p(S+12)p(S1)='+Sright20.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+20)p(S+12)p(S2)='+Sright20.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+20)p(S+20)p(S0)='+Sright20.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+20)p(S+20)p(S1)='+Sright20.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+20)p(S+20)p(S2)='+Sright20.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+20)p(S+21)p(S0)='+Sright20.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+20)p(S+21)p(S1)='+Sright20.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+20)p(S+21)p(S2)='+Sright20.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+20)p(S+22)p(S0)='+Sright20.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+20)p(S+22)p(S1)='+Sright20.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+20)p(S+22)p(S2)='+Sright20.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+20)p(S+30)p(S0)='+Sright20.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+20)p(S+30)p(S1)='+Sright20.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+20)p(S+30)p(S2)='+Sright20.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+20)p(S+31)p(S0)='+Sright20.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+20)p(S+31)p(S1)='+Sright20.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+20)p(S+31)p(S2)='+Sright20.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+20)p(S+32)p(S0)='+Sright20.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+20)p(S+32)p(S1)='+Sright20.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+20)p(S+32)p(S2)='+Sright20.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+20)p(S+40)p(S0)='+Sright20.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+20)p(S+40)p(S1)='+Sright20.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+20)p(S+40)p(S2)='+Sright20.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+20)p(S+41)p(S0)='+Sright20.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+20)p(S+41)p(S1)='+Sright20.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+20)p(S+41)p(S2)='+Sright20.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+20)p(S+42)p(S0)='+Sright20.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+20)p(S+42)p(S1)='+Sright20.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+20)p(S+42)p(S2)='+Sright20.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+20)w(S+10)p(S0)='+Sright20.lemma+Sright10.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+20)w(S+10)p(S1)='+Sright20.lemma+Sright10.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+20)w(S+10)p(S2)='+Sright20.lemma+Sright10.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+20)w(S+11)p(S0)='+Sright20.lemma+Sright11.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+20)w(S+11)p(S1)='+Sright20.lemma+Sright11.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+20)w(S+11)p(S2)='+Sright20.lemma+Sright11.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+20)w(S+12)p(S0)='+Sright20.lemma+Sright12.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+20)w(S+12)p(S1)='+Sright20.lemma+Sright12.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+20)w(S+12)p(S2)='+Sright20.lemma+Sright12.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+20)w(S+20)p(S0)='+Sright20.lemma+Sright20.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+20)w(S+20)p(S1)='+Sright20.lemma+Sright20.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+20)w(S+20)p(S2)='+Sright20.lemma+Sright20.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+20)w(S+21)p(S0)='+Sright20.lemma+Sright21.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+20)w(S+21)p(S1)='+Sright20.lemma+Sright21.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+20)w(S+21)p(S2)='+Sright20.lemma+Sright21.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+20)w(S+22)p(S0)='+Sright20.lemma+Sright22.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+20)w(S+22)p(S1)='+Sright20.lemma+Sright22.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+20)w(S+22)p(S2)='+Sright20.lemma+Sright22.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+20)w(S+30)p(S0)='+Sright20.lemma+Sright30.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+20)w(S+30)p(S1)='+Sright20.lemma+Sright30.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+20)w(S+30)p(S2)='+Sright20.lemma+Sright30.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+20)w(S+31)p(S0)='+Sright20.lemma+Sright31.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+20)w(S+31)p(S1)='+Sright20.lemma+Sright31.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+20)w(S+31)p(S2)='+Sright20.lemma+Sright31.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+20)w(S+32)p(S0)='+Sright20.lemma+Sright32.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+20)w(S+32)p(S1)='+Sright20.lemma+Sright32.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+20)w(S+32)p(S2)='+Sright20.lemma+Sright32.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+20)w(S+40)p(S0)='+Sright20.lemma+Sright40.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+20)w(S+40)p(S1)='+Sright20.lemma+Sright40.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+20)w(S+40)p(S2)='+Sright20.lemma+Sright40.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+20)w(S+41)p(S0)='+Sright20.lemma+Sright41.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+20)w(S+41)p(S1)='+Sright20.lemma+Sright41.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+20)w(S+41)p(S2)='+Sright20.lemma+Sright41.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+20)w(S+42)p(S0)='+Sright20.lemma+Sright42.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+20)w(S+42)p(S1)='+Sright20.lemma+Sright42.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+20)w(S+42)p(S2)='+Sright20.lemma+Sright42.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+21)l(S+10)p(S0)='+Sright21.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+21)l(S+10)p(S1)='+Sright21.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+21)l(S+10)p(S2)='+Sright21.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+21)l(S+11)p(S0)='+Sright21.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+21)l(S+11)p(S1)='+Sright21.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+21)l(S+11)p(S2)='+Sright21.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+21)l(S+12)p(S0)='+Sright21.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+21)l(S+12)p(S1)='+Sright21.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+21)l(S+12)p(S2)='+Sright21.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+21)l(S+20)p(S0)='+Sright21.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+21)l(S+20)p(S1)='+Sright21.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+21)l(S+20)p(S2)='+Sright21.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+21)l(S+21)p(S0)='+Sright21.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+21)l(S+21)p(S1)='+Sright21.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+21)l(S+21)p(S2)='+Sright21.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+21)l(S+22)p(S0)='+Sright21.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+21)l(S+22)p(S1)='+Sright21.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+21)l(S+22)p(S2)='+Sright21.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+21)l(S+30)p(S0)='+Sright21.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+21)l(S+30)p(S1)='+Sright21.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+21)l(S+30)p(S2)='+Sright21.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+21)l(S+31)p(S0)='+Sright21.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+21)l(S+31)p(S1)='+Sright21.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+21)l(S+31)p(S2)='+Sright21.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+21)l(S+32)p(S0)='+Sright21.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+21)l(S+32)p(S1)='+Sright21.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+21)l(S+32)p(S2)='+Sright21.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+21)l(S+40)p(S0)='+Sright21.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+21)l(S+40)p(S1)='+Sright21.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+21)l(S+40)p(S2)='+Sright21.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+21)l(S+41)p(S0)='+Sright21.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+21)l(S+41)p(S1)='+Sright21.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+21)l(S+41)p(S2)='+Sright21.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+21)l(S+42)p(S0)='+Sright21.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+21)l(S+42)p(S1)='+Sright21.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+21)l(S+42)p(S2)='+Sright21.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+21)p(S+10)p(S0)='+Sright21.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+21)p(S+10)p(S1)='+Sright21.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+21)p(S+10)p(S2)='+Sright21.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+21)p(S+11)p(S0)='+Sright21.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+21)p(S+11)p(S1)='+Sright21.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+21)p(S+11)p(S2)='+Sright21.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+21)p(S+12)p(S0)='+Sright21.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+21)p(S+12)p(S1)='+Sright21.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+21)p(S+12)p(S2)='+Sright21.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+21)p(S+20)p(S0)='+Sright21.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+21)p(S+20)p(S1)='+Sright21.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+21)p(S+20)p(S2)='+Sright21.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+21)p(S+21)p(S0)='+Sright21.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+21)p(S+21)p(S1)='+Sright21.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+21)p(S+21)p(S2)='+Sright21.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+21)p(S+22)p(S0)='+Sright21.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+21)p(S+22)p(S1)='+Sright21.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+21)p(S+22)p(S2)='+Sright21.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+21)p(S+30)p(S0)='+Sright21.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+21)p(S+30)p(S1)='+Sright21.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+21)p(S+30)p(S2)='+Sright21.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+21)p(S+31)p(S0)='+Sright21.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+21)p(S+31)p(S1)='+Sright21.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+21)p(S+31)p(S2)='+Sright21.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+21)p(S+32)p(S0)='+Sright21.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+21)p(S+32)p(S1)='+Sright21.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+21)p(S+32)p(S2)='+Sright21.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+21)p(S+40)p(S0)='+Sright21.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+21)p(S+40)p(S1)='+Sright21.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+21)p(S+40)p(S2)='+Sright21.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+21)p(S+41)p(S0)='+Sright21.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+21)p(S+41)p(S1)='+Sright21.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+21)p(S+41)p(S2)='+Sright21.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+21)p(S+42)p(S0)='+Sright21.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+21)p(S+42)p(S1)='+Sright21.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+21)p(S+42)p(S2)='+Sright21.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+21)w(S+10)p(S0)='+Sright21.lemma+Sright10.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+21)w(S+10)p(S1)='+Sright21.lemma+Sright10.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+21)w(S+10)p(S2)='+Sright21.lemma+Sright10.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+21)w(S+11)p(S0)='+Sright21.lemma+Sright11.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+21)w(S+11)p(S1)='+Sright21.lemma+Sright11.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+21)w(S+11)p(S2)='+Sright21.lemma+Sright11.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+21)w(S+12)p(S0)='+Sright21.lemma+Sright12.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+21)w(S+12)p(S1)='+Sright21.lemma+Sright12.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+21)w(S+12)p(S2)='+Sright21.lemma+Sright12.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+21)w(S+20)p(S0)='+Sright21.lemma+Sright20.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+21)w(S+20)p(S1)='+Sright21.lemma+Sright20.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+21)w(S+20)p(S2)='+Sright21.lemma+Sright20.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+21)w(S+21)p(S0)='+Sright21.lemma+Sright21.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+21)w(S+21)p(S1)='+Sright21.lemma+Sright21.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+21)w(S+21)p(S2)='+Sright21.lemma+Sright21.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+21)w(S+22)p(S0)='+Sright21.lemma+Sright22.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+21)w(S+22)p(S1)='+Sright21.lemma+Sright22.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+21)w(S+22)p(S2)='+Sright21.lemma+Sright22.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+21)w(S+30)p(S0)='+Sright21.lemma+Sright30.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+21)w(S+30)p(S1)='+Sright21.lemma+Sright30.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+21)w(S+30)p(S2)='+Sright21.lemma+Sright30.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+21)w(S+31)p(S0)='+Sright21.lemma+Sright31.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+21)w(S+31)p(S1)='+Sright21.lemma+Sright31.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+21)w(S+31)p(S2)='+Sright21.lemma+Sright31.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+21)w(S+32)p(S0)='+Sright21.lemma+Sright32.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+21)w(S+32)p(S1)='+Sright21.lemma+Sright32.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+21)w(S+32)p(S2)='+Sright21.lemma+Sright32.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+21)w(S+40)p(S0)='+Sright21.lemma+Sright40.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+21)w(S+40)p(S1)='+Sright21.lemma+Sright40.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+21)w(S+40)p(S2)='+Sright21.lemma+Sright40.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+21)w(S+41)p(S0)='+Sright21.lemma+Sright41.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+21)w(S+41)p(S1)='+Sright21.lemma+Sright41.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+21)w(S+41)p(S2)='+Sright21.lemma+Sright41.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+21)w(S+42)p(S0)='+Sright21.lemma+Sright42.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+21)w(S+42)p(S1)='+Sright21.lemma+Sright42.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+21)w(S+42)p(S2)='+Sright21.lemma+Sright42.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+22)l(S+10)p(S0)='+Sright22.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+22)l(S+10)p(S1)='+Sright22.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+22)l(S+10)p(S2)='+Sright22.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+22)l(S+11)p(S0)='+Sright22.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+22)l(S+11)p(S1)='+Sright22.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+22)l(S+11)p(S2)='+Sright22.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+22)l(S+12)p(S0)='+Sright22.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+22)l(S+12)p(S1)='+Sright22.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+22)l(S+12)p(S2)='+Sright22.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+22)l(S+20)p(S0)='+Sright22.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+22)l(S+20)p(S1)='+Sright22.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+22)l(S+20)p(S2)='+Sright22.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+22)l(S+21)p(S0)='+Sright22.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+22)l(S+21)p(S1)='+Sright22.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+22)l(S+21)p(S2)='+Sright22.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+22)l(S+22)p(S0)='+Sright22.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+22)l(S+22)p(S1)='+Sright22.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+22)l(S+22)p(S2)='+Sright22.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+22)l(S+30)p(S0)='+Sright22.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+22)l(S+30)p(S1)='+Sright22.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+22)l(S+30)p(S2)='+Sright22.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+22)l(S+31)p(S0)='+Sright22.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+22)l(S+31)p(S1)='+Sright22.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+22)l(S+31)p(S2)='+Sright22.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+22)l(S+32)p(S0)='+Sright22.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+22)l(S+32)p(S1)='+Sright22.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+22)l(S+32)p(S2)='+Sright22.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+22)l(S+40)p(S0)='+Sright22.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+22)l(S+40)p(S1)='+Sright22.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+22)l(S+40)p(S2)='+Sright22.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+22)l(S+41)p(S0)='+Sright22.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+22)l(S+41)p(S1)='+Sright22.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+22)l(S+41)p(S2)='+Sright22.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+22)l(S+42)p(S0)='+Sright22.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+22)l(S+42)p(S1)='+Sright22.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+22)l(S+42)p(S2)='+Sright22.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+22)p(S+10)p(S0)='+Sright22.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+22)p(S+10)p(S1)='+Sright22.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+22)p(S+10)p(S2)='+Sright22.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+22)p(S+11)p(S0)='+Sright22.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+22)p(S+11)p(S1)='+Sright22.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+22)p(S+11)p(S2)='+Sright22.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+22)p(S+12)p(S0)='+Sright22.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+22)p(S+12)p(S1)='+Sright22.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+22)p(S+12)p(S2)='+Sright22.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+22)p(S+20)p(S0)='+Sright22.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+22)p(S+20)p(S1)='+Sright22.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+22)p(S+20)p(S2)='+Sright22.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+22)p(S+21)p(S0)='+Sright22.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+22)p(S+21)p(S1)='+Sright22.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+22)p(S+21)p(S2)='+Sright22.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+22)p(S+22)p(S0)='+Sright22.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+22)p(S+22)p(S1)='+Sright22.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+22)p(S+22)p(S2)='+Sright22.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+22)p(S+30)p(S0)='+Sright22.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+22)p(S+30)p(S1)='+Sright22.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+22)p(S+30)p(S2)='+Sright22.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+22)p(S+31)p(S0)='+Sright22.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+22)p(S+31)p(S1)='+Sright22.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+22)p(S+31)p(S2)='+Sright22.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+22)p(S+32)p(S0)='+Sright22.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+22)p(S+32)p(S1)='+Sright22.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+22)p(S+32)p(S2)='+Sright22.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+22)p(S+40)p(S0)='+Sright22.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+22)p(S+40)p(S1)='+Sright22.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+22)p(S+40)p(S2)='+Sright22.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+22)p(S+41)p(S0)='+Sright22.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+22)p(S+41)p(S1)='+Sright22.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+22)p(S+41)p(S2)='+Sright22.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+22)p(S+42)p(S0)='+Sright22.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+22)p(S+42)p(S1)='+Sright22.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+22)p(S+42)p(S2)='+Sright22.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+22)w(S+10)p(S0)='+Sright22.lemma+Sright10.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+22)w(S+10)p(S1)='+Sright22.lemma+Sright10.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+22)w(S+10)p(S2)='+Sright22.lemma+Sright10.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+22)w(S+11)p(S0)='+Sright22.lemma+Sright11.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+22)w(S+11)p(S1)='+Sright22.lemma+Sright11.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+22)w(S+11)p(S2)='+Sright22.lemma+Sright11.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+22)w(S+12)p(S0)='+Sright22.lemma+Sright12.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+22)w(S+12)p(S1)='+Sright22.lemma+Sright12.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+22)w(S+12)p(S2)='+Sright22.lemma+Sright12.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+22)w(S+20)p(S0)='+Sright22.lemma+Sright20.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+22)w(S+20)p(S1)='+Sright22.lemma+Sright20.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+22)w(S+20)p(S2)='+Sright22.lemma+Sright20.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+22)w(S+21)p(S0)='+Sright22.lemma+Sright21.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+22)w(S+21)p(S1)='+Sright22.lemma+Sright21.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+22)w(S+21)p(S2)='+Sright22.lemma+Sright21.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+22)w(S+22)p(S0)='+Sright22.lemma+Sright22.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+22)w(S+22)p(S1)='+Sright22.lemma+Sright22.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+22)w(S+22)p(S2)='+Sright22.lemma+Sright22.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+22)w(S+30)p(S0)='+Sright22.lemma+Sright30.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+22)w(S+30)p(S1)='+Sright22.lemma+Sright30.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+22)w(S+30)p(S2)='+Sright22.lemma+Sright30.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+22)w(S+31)p(S0)='+Sright22.lemma+Sright31.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+22)w(S+31)p(S1)='+Sright22.lemma+Sright31.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+22)w(S+31)p(S2)='+Sright22.lemma+Sright31.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+22)w(S+32)p(S0)='+Sright22.lemma+Sright32.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+22)w(S+32)p(S1)='+Sright22.lemma+Sright32.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+22)w(S+32)p(S2)='+Sright22.lemma+Sright32.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+22)w(S+40)p(S0)='+Sright22.lemma+Sright40.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+22)w(S+40)p(S1)='+Sright22.lemma+Sright40.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+22)w(S+40)p(S2)='+Sright22.lemma+Sright40.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+22)w(S+41)p(S0)='+Sright22.lemma+Sright41.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+22)w(S+41)p(S1)='+Sright22.lemma+Sright41.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+22)w(S+41)p(S2)='+Sright22.lemma+Sright41.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+22)w(S+42)p(S0)='+Sright22.lemma+Sright42.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+22)w(S+42)p(S1)='+Sright22.lemma+Sright42.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+22)w(S+42)p(S2)='+Sright22.lemma+Sright42.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+30)l(S+10)p(S0)='+Sright30.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+30)l(S+10)p(S1)='+Sright30.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+30)l(S+10)p(S2)='+Sright30.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+30)l(S+11)p(S0)='+Sright30.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+30)l(S+11)p(S1)='+Sright30.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+30)l(S+11)p(S2)='+Sright30.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+30)l(S+12)p(S0)='+Sright30.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+30)l(S+12)p(S1)='+Sright30.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+30)l(S+12)p(S2)='+Sright30.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+30)l(S+20)p(S0)='+Sright30.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+30)l(S+20)p(S1)='+Sright30.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+30)l(S+20)p(S2)='+Sright30.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+30)l(S+21)p(S0)='+Sright30.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+30)l(S+21)p(S1)='+Sright30.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+30)l(S+21)p(S2)='+Sright30.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+30)l(S+22)p(S0)='+Sright30.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+30)l(S+22)p(S1)='+Sright30.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+30)l(S+22)p(S2)='+Sright30.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+30)l(S+30)p(S0)='+Sright30.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+30)l(S+30)p(S1)='+Sright30.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+30)l(S+30)p(S2)='+Sright30.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+30)l(S+31)p(S0)='+Sright30.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+30)l(S+31)p(S1)='+Sright30.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+30)l(S+31)p(S2)='+Sright30.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+30)l(S+32)p(S0)='+Sright30.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+30)l(S+32)p(S1)='+Sright30.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+30)l(S+32)p(S2)='+Sright30.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+30)l(S+40)p(S0)='+Sright30.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+30)l(S+40)p(S1)='+Sright30.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+30)l(S+40)p(S2)='+Sright30.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+30)l(S+41)p(S0)='+Sright30.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+30)l(S+41)p(S1)='+Sright30.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+30)l(S+41)p(S2)='+Sright30.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+30)l(S+42)p(S0)='+Sright30.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+30)l(S+42)p(S1)='+Sright30.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+30)l(S+42)p(S2)='+Sright30.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+30)p(S+10)p(S0)='+Sright30.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+30)p(S+10)p(S1)='+Sright30.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+30)p(S+10)p(S2)='+Sright30.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+30)p(S+11)p(S0)='+Sright30.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+30)p(S+11)p(S1)='+Sright30.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+30)p(S+11)p(S2)='+Sright30.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+30)p(S+12)p(S0)='+Sright30.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+30)p(S+12)p(S1)='+Sright30.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+30)p(S+12)p(S2)='+Sright30.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+30)p(S+20)p(S0)='+Sright30.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+30)p(S+20)p(S1)='+Sright30.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+30)p(S+20)p(S2)='+Sright30.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+30)p(S+21)p(S0)='+Sright30.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+30)p(S+21)p(S1)='+Sright30.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+30)p(S+21)p(S2)='+Sright30.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+30)p(S+22)p(S0)='+Sright30.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+30)p(S+22)p(S1)='+Sright30.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+30)p(S+22)p(S2)='+Sright30.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+30)p(S+30)p(S0)='+Sright30.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+30)p(S+30)p(S1)='+Sright30.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+30)p(S+30)p(S2)='+Sright30.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+30)p(S+31)p(S0)='+Sright30.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+30)p(S+31)p(S1)='+Sright30.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+30)p(S+31)p(S2)='+Sright30.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+30)p(S+32)p(S0)='+Sright30.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+30)p(S+32)p(S1)='+Sright30.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+30)p(S+32)p(S2)='+Sright30.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+30)p(S+40)p(S0)='+Sright30.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+30)p(S+40)p(S1)='+Sright30.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+30)p(S+40)p(S2)='+Sright30.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+30)p(S+41)p(S0)='+Sright30.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+30)p(S+41)p(S1)='+Sright30.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+30)p(S+41)p(S2)='+Sright30.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+30)p(S+42)p(S0)='+Sright30.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+30)p(S+42)p(S1)='+Sright30.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+30)p(S+42)p(S2)='+Sright30.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+30)w(S+10)p(S0)='+Sright30.lemma+Sright10.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+30)w(S+10)p(S1)='+Sright30.lemma+Sright10.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+30)w(S+10)p(S2)='+Sright30.lemma+Sright10.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+30)w(S+11)p(S0)='+Sright30.lemma+Sright11.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+30)w(S+11)p(S1)='+Sright30.lemma+Sright11.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+30)w(S+11)p(S2)='+Sright30.lemma+Sright11.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+30)w(S+12)p(S0)='+Sright30.lemma+Sright12.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+30)w(S+12)p(S1)='+Sright30.lemma+Sright12.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+30)w(S+12)p(S2)='+Sright30.lemma+Sright12.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+30)w(S+20)p(S0)='+Sright30.lemma+Sright20.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+30)w(S+20)p(S1)='+Sright30.lemma+Sright20.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+30)w(S+20)p(S2)='+Sright30.lemma+Sright20.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+30)w(S+21)p(S0)='+Sright30.lemma+Sright21.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+30)w(S+21)p(S1)='+Sright30.lemma+Sright21.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+30)w(S+21)p(S2)='+Sright30.lemma+Sright21.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+30)w(S+22)p(S0)='+Sright30.lemma+Sright22.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+30)w(S+22)p(S1)='+Sright30.lemma+Sright22.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+30)w(S+22)p(S2)='+Sright30.lemma+Sright22.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+30)w(S+30)p(S0)='+Sright30.lemma+Sright30.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+30)w(S+30)p(S1)='+Sright30.lemma+Sright30.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+30)w(S+30)p(S2)='+Sright30.lemma+Sright30.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+30)w(S+31)p(S0)='+Sright30.lemma+Sright31.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+30)w(S+31)p(S1)='+Sright30.lemma+Sright31.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+30)w(S+31)p(S2)='+Sright30.lemma+Sright31.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+30)w(S+32)p(S0)='+Sright30.lemma+Sright32.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+30)w(S+32)p(S1)='+Sright30.lemma+Sright32.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+30)w(S+32)p(S2)='+Sright30.lemma+Sright32.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+30)w(S+40)p(S0)='+Sright30.lemma+Sright40.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+30)w(S+40)p(S1)='+Sright30.lemma+Sright40.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+30)w(S+40)p(S2)='+Sright30.lemma+Sright40.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+30)w(S+41)p(S0)='+Sright30.lemma+Sright41.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+30)w(S+41)p(S1)='+Sright30.lemma+Sright41.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+30)w(S+41)p(S2)='+Sright30.lemma+Sright41.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+30)w(S+42)p(S0)='+Sright30.lemma+Sright42.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+30)w(S+42)p(S1)='+Sright30.lemma+Sright42.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+30)w(S+42)p(S2)='+Sright30.lemma+Sright42.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+31)l(S+10)p(S0)='+Sright31.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+31)l(S+10)p(S1)='+Sright31.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+31)l(S+10)p(S2)='+Sright31.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+31)l(S+11)p(S0)='+Sright31.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+31)l(S+11)p(S1)='+Sright31.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+31)l(S+11)p(S2)='+Sright31.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+31)l(S+12)p(S0)='+Sright31.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+31)l(S+12)p(S1)='+Sright31.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+31)l(S+12)p(S2)='+Sright31.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+31)l(S+20)p(S0)='+Sright31.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+31)l(S+20)p(S1)='+Sright31.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+31)l(S+20)p(S2)='+Sright31.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+31)l(S+21)p(S0)='+Sright31.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+31)l(S+21)p(S1)='+Sright31.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+31)l(S+21)p(S2)='+Sright31.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+31)l(S+22)p(S0)='+Sright31.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+31)l(S+22)p(S1)='+Sright31.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+31)l(S+22)p(S2)='+Sright31.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+31)l(S+30)p(S0)='+Sright31.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+31)l(S+30)p(S1)='+Sright31.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+31)l(S+30)p(S2)='+Sright31.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+31)l(S+31)p(S0)='+Sright31.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+31)l(S+31)p(S1)='+Sright31.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+31)l(S+31)p(S2)='+Sright31.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+31)l(S+32)p(S0)='+Sright31.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+31)l(S+32)p(S1)='+Sright31.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+31)l(S+32)p(S2)='+Sright31.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+31)l(S+40)p(S0)='+Sright31.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+31)l(S+40)p(S1)='+Sright31.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+31)l(S+40)p(S2)='+Sright31.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+31)l(S+41)p(S0)='+Sright31.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+31)l(S+41)p(S1)='+Sright31.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+31)l(S+41)p(S2)='+Sright31.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+31)l(S+42)p(S0)='+Sright31.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+31)l(S+42)p(S1)='+Sright31.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+31)l(S+42)p(S2)='+Sright31.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+31)p(S+10)p(S0)='+Sright31.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+31)p(S+10)p(S1)='+Sright31.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+31)p(S+10)p(S2)='+Sright31.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+31)p(S+11)p(S0)='+Sright31.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+31)p(S+11)p(S1)='+Sright31.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+31)p(S+11)p(S2)='+Sright31.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+31)p(S+12)p(S0)='+Sright31.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+31)p(S+12)p(S1)='+Sright31.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+31)p(S+12)p(S2)='+Sright31.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+31)p(S+20)p(S0)='+Sright31.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+31)p(S+20)p(S1)='+Sright31.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+31)p(S+20)p(S2)='+Sright31.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+31)p(S+21)p(S0)='+Sright31.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+31)p(S+21)p(S1)='+Sright31.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+31)p(S+21)p(S2)='+Sright31.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+31)p(S+22)p(S0)='+Sright31.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+31)p(S+22)p(S1)='+Sright31.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+31)p(S+22)p(S2)='+Sright31.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+31)p(S+30)p(S0)='+Sright31.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+31)p(S+30)p(S1)='+Sright31.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+31)p(S+30)p(S2)='+Sright31.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+31)p(S+31)p(S0)='+Sright31.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+31)p(S+31)p(S1)='+Sright31.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+31)p(S+31)p(S2)='+Sright31.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+31)p(S+32)p(S0)='+Sright31.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+31)p(S+32)p(S1)='+Sright31.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+31)p(S+32)p(S2)='+Sright31.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+31)p(S+40)p(S0)='+Sright31.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+31)p(S+40)p(S1)='+Sright31.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+31)p(S+40)p(S2)='+Sright31.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+31)p(S+41)p(S0)='+Sright31.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+31)p(S+41)p(S1)='+Sright31.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+31)p(S+41)p(S2)='+Sright31.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+31)p(S+42)p(S0)='+Sright31.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+31)p(S+42)p(S1)='+Sright31.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+31)p(S+42)p(S2)='+Sright31.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+31)w(S+10)p(S0)='+Sright31.lemma+Sright10.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+31)w(S+10)p(S1)='+Sright31.lemma+Sright10.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+31)w(S+10)p(S2)='+Sright31.lemma+Sright10.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+31)w(S+11)p(S0)='+Sright31.lemma+Sright11.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+31)w(S+11)p(S1)='+Sright31.lemma+Sright11.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+31)w(S+11)p(S2)='+Sright31.lemma+Sright11.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+31)w(S+12)p(S0)='+Sright31.lemma+Sright12.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+31)w(S+12)p(S1)='+Sright31.lemma+Sright12.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+31)w(S+12)p(S2)='+Sright31.lemma+Sright12.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+31)w(S+20)p(S0)='+Sright31.lemma+Sright20.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+31)w(S+20)p(S1)='+Sright31.lemma+Sright20.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+31)w(S+20)p(S2)='+Sright31.lemma+Sright20.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+31)w(S+21)p(S0)='+Sright31.lemma+Sright21.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+31)w(S+21)p(S1)='+Sright31.lemma+Sright21.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+31)w(S+21)p(S2)='+Sright31.lemma+Sright21.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+31)w(S+22)p(S0)='+Sright31.lemma+Sright22.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+31)w(S+22)p(S1)='+Sright31.lemma+Sright22.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+31)w(S+22)p(S2)='+Sright31.lemma+Sright22.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+31)w(S+30)p(S0)='+Sright31.lemma+Sright30.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+31)w(S+30)p(S1)='+Sright31.lemma+Sright30.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+31)w(S+30)p(S2)='+Sright31.lemma+Sright30.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+31)w(S+31)p(S0)='+Sright31.lemma+Sright31.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+31)w(S+31)p(S1)='+Sright31.lemma+Sright31.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+31)w(S+31)p(S2)='+Sright31.lemma+Sright31.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+31)w(S+32)p(S0)='+Sright31.lemma+Sright32.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+31)w(S+32)p(S1)='+Sright31.lemma+Sright32.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+31)w(S+32)p(S2)='+Sright31.lemma+Sright32.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+31)w(S+40)p(S0)='+Sright31.lemma+Sright40.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+31)w(S+40)p(S1)='+Sright31.lemma+Sright40.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+31)w(S+40)p(S2)='+Sright31.lemma+Sright40.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+31)w(S+41)p(S0)='+Sright31.lemma+Sright41.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+31)w(S+41)p(S1)='+Sright31.lemma+Sright41.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+31)w(S+41)p(S2)='+Sright31.lemma+Sright41.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+31)w(S+42)p(S0)='+Sright31.lemma+Sright42.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+31)w(S+42)p(S1)='+Sright31.lemma+Sright42.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+31)w(S+42)p(S2)='+Sright31.lemma+Sright42.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+32)l(S+10)p(S0)='+Sright32.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+32)l(S+10)p(S1)='+Sright32.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+32)l(S+10)p(S2)='+Sright32.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+32)l(S+11)p(S0)='+Sright32.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+32)l(S+11)p(S1)='+Sright32.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+32)l(S+11)p(S2)='+Sright32.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+32)l(S+12)p(S0)='+Sright32.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+32)l(S+12)p(S1)='+Sright32.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+32)l(S+12)p(S2)='+Sright32.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+32)l(S+20)p(S0)='+Sright32.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+32)l(S+20)p(S1)='+Sright32.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+32)l(S+20)p(S2)='+Sright32.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+32)l(S+21)p(S0)='+Sright32.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+32)l(S+21)p(S1)='+Sright32.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+32)l(S+21)p(S2)='+Sright32.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+32)l(S+22)p(S0)='+Sright32.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+32)l(S+22)p(S1)='+Sright32.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+32)l(S+22)p(S2)='+Sright32.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+32)l(S+30)p(S0)='+Sright32.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+32)l(S+30)p(S1)='+Sright32.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+32)l(S+30)p(S2)='+Sright32.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+32)l(S+31)p(S0)='+Sright32.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+32)l(S+31)p(S1)='+Sright32.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+32)l(S+31)p(S2)='+Sright32.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+32)l(S+32)p(S0)='+Sright32.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+32)l(S+32)p(S1)='+Sright32.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+32)l(S+32)p(S2)='+Sright32.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+32)l(S+40)p(S0)='+Sright32.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+32)l(S+40)p(S1)='+Sright32.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+32)l(S+40)p(S2)='+Sright32.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+32)l(S+41)p(S0)='+Sright32.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+32)l(S+41)p(S1)='+Sright32.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+32)l(S+41)p(S2)='+Sright32.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+32)l(S+42)p(S0)='+Sright32.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+32)l(S+42)p(S1)='+Sright32.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+32)l(S+42)p(S2)='+Sright32.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+32)p(S+10)p(S0)='+Sright32.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+32)p(S+10)p(S1)='+Sright32.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+32)p(S+10)p(S2)='+Sright32.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+32)p(S+11)p(S0)='+Sright32.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+32)p(S+11)p(S1)='+Sright32.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+32)p(S+11)p(S2)='+Sright32.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+32)p(S+12)p(S0)='+Sright32.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+32)p(S+12)p(S1)='+Sright32.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+32)p(S+12)p(S2)='+Sright32.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+32)p(S+20)p(S0)='+Sright32.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+32)p(S+20)p(S1)='+Sright32.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+32)p(S+20)p(S2)='+Sright32.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+32)p(S+21)p(S0)='+Sright32.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+32)p(S+21)p(S1)='+Sright32.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+32)p(S+21)p(S2)='+Sright32.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+32)p(S+22)p(S0)='+Sright32.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+32)p(S+22)p(S1)='+Sright32.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+32)p(S+22)p(S2)='+Sright32.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+32)p(S+30)p(S0)='+Sright32.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+32)p(S+30)p(S1)='+Sright32.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+32)p(S+30)p(S2)='+Sright32.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+32)p(S+31)p(S0)='+Sright32.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+32)p(S+31)p(S1)='+Sright32.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+32)p(S+31)p(S2)='+Sright32.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+32)p(S+32)p(S0)='+Sright32.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+32)p(S+32)p(S1)='+Sright32.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+32)p(S+32)p(S2)='+Sright32.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+32)p(S+40)p(S0)='+Sright32.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+32)p(S+40)p(S1)='+Sright32.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+32)p(S+40)p(S2)='+Sright32.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+32)p(S+41)p(S0)='+Sright32.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+32)p(S+41)p(S1)='+Sright32.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+32)p(S+41)p(S2)='+Sright32.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+32)p(S+42)p(S0)='+Sright32.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+32)p(S+42)p(S1)='+Sright32.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+32)p(S+42)p(S2)='+Sright32.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+32)w(S+10)p(S0)='+Sright32.lemma+Sright10.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+32)w(S+10)p(S1)='+Sright32.lemma+Sright10.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+32)w(S+10)p(S2)='+Sright32.lemma+Sright10.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+32)w(S+11)p(S0)='+Sright32.lemma+Sright11.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+32)w(S+11)p(S1)='+Sright32.lemma+Sright11.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+32)w(S+11)p(S2)='+Sright32.lemma+Sright11.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+32)w(S+12)p(S0)='+Sright32.lemma+Sright12.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+32)w(S+12)p(S1)='+Sright32.lemma+Sright12.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+32)w(S+12)p(S2)='+Sright32.lemma+Sright12.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+32)w(S+20)p(S0)='+Sright32.lemma+Sright20.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+32)w(S+20)p(S1)='+Sright32.lemma+Sright20.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+32)w(S+20)p(S2)='+Sright32.lemma+Sright20.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+32)w(S+21)p(S0)='+Sright32.lemma+Sright21.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+32)w(S+21)p(S1)='+Sright32.lemma+Sright21.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+32)w(S+21)p(S2)='+Sright32.lemma+Sright21.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+32)w(S+22)p(S0)='+Sright32.lemma+Sright22.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+32)w(S+22)p(S1)='+Sright32.lemma+Sright22.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+32)w(S+22)p(S2)='+Sright32.lemma+Sright22.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+32)w(S+30)p(S0)='+Sright32.lemma+Sright30.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+32)w(S+30)p(S1)='+Sright32.lemma+Sright30.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+32)w(S+30)p(S2)='+Sright32.lemma+Sright30.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+32)w(S+31)p(S0)='+Sright32.lemma+Sright31.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+32)w(S+31)p(S1)='+Sright32.lemma+Sright31.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+32)w(S+31)p(S2)='+Sright32.lemma+Sright31.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+32)w(S+32)p(S0)='+Sright32.lemma+Sright32.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+32)w(S+32)p(S1)='+Sright32.lemma+Sright32.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+32)w(S+32)p(S2)='+Sright32.lemma+Sright32.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+32)w(S+40)p(S0)='+Sright32.lemma+Sright40.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+32)w(S+40)p(S1)='+Sright32.lemma+Sright40.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+32)w(S+40)p(S2)='+Sright32.lemma+Sright40.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+32)w(S+41)p(S0)='+Sright32.lemma+Sright41.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+32)w(S+41)p(S1)='+Sright32.lemma+Sright41.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+32)w(S+41)p(S2)='+Sright32.lemma+Sright41.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+32)w(S+42)p(S0)='+Sright32.lemma+Sright42.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+32)w(S+42)p(S1)='+Sright32.lemma+Sright42.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+32)w(S+42)p(S2)='+Sright32.lemma+Sright42.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+40)l(S+10)p(S0)='+Sright40.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+40)l(S+10)p(S1)='+Sright40.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+40)l(S+10)p(S2)='+Sright40.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+40)l(S+11)p(S0)='+Sright40.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+40)l(S+11)p(S1)='+Sright40.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+40)l(S+11)p(S2)='+Sright40.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+40)l(S+12)p(S0)='+Sright40.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+40)l(S+12)p(S1)='+Sright40.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+40)l(S+12)p(S2)='+Sright40.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+40)l(S+20)p(S0)='+Sright40.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+40)l(S+20)p(S1)='+Sright40.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+40)l(S+20)p(S2)='+Sright40.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+40)l(S+21)p(S0)='+Sright40.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+40)l(S+21)p(S1)='+Sright40.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+40)l(S+21)p(S2)='+Sright40.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+40)l(S+22)p(S0)='+Sright40.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+40)l(S+22)p(S1)='+Sright40.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+40)l(S+22)p(S2)='+Sright40.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+40)l(S+30)p(S0)='+Sright40.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+40)l(S+30)p(S1)='+Sright40.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+40)l(S+30)p(S2)='+Sright40.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+40)l(S+31)p(S0)='+Sright40.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+40)l(S+31)p(S1)='+Sright40.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+40)l(S+31)p(S2)='+Sright40.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+40)l(S+32)p(S0)='+Sright40.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+40)l(S+32)p(S1)='+Sright40.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+40)l(S+32)p(S2)='+Sright40.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+40)l(S+40)p(S0)='+Sright40.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+40)l(S+40)p(S1)='+Sright40.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+40)l(S+40)p(S2)='+Sright40.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+40)l(S+41)p(S0)='+Sright40.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+40)l(S+41)p(S1)='+Sright40.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+40)l(S+41)p(S2)='+Sright40.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+40)l(S+42)p(S0)='+Sright40.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+40)l(S+42)p(S1)='+Sright40.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+40)l(S+42)p(S2)='+Sright40.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+40)p(S+10)p(S0)='+Sright40.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+40)p(S+10)p(S1)='+Sright40.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+40)p(S+10)p(S2)='+Sright40.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+40)p(S+11)p(S0)='+Sright40.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+40)p(S+11)p(S1)='+Sright40.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+40)p(S+11)p(S2)='+Sright40.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+40)p(S+12)p(S0)='+Sright40.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+40)p(S+12)p(S1)='+Sright40.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+40)p(S+12)p(S2)='+Sright40.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+40)p(S+20)p(S0)='+Sright40.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+40)p(S+20)p(S1)='+Sright40.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+40)p(S+20)p(S2)='+Sright40.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+40)p(S+21)p(S0)='+Sright40.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+40)p(S+21)p(S1)='+Sright40.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+40)p(S+21)p(S2)='+Sright40.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+40)p(S+22)p(S0)='+Sright40.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+40)p(S+22)p(S1)='+Sright40.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+40)p(S+22)p(S2)='+Sright40.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+40)p(S+30)p(S0)='+Sright40.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+40)p(S+30)p(S1)='+Sright40.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+40)p(S+30)p(S2)='+Sright40.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+40)p(S+31)p(S0)='+Sright40.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+40)p(S+31)p(S1)='+Sright40.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+40)p(S+31)p(S2)='+Sright40.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+40)p(S+32)p(S0)='+Sright40.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+40)p(S+32)p(S1)='+Sright40.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+40)p(S+32)p(S2)='+Sright40.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+40)p(S+40)p(S0)='+Sright40.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+40)p(S+40)p(S1)='+Sright40.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+40)p(S+40)p(S2)='+Sright40.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+40)p(S+41)p(S0)='+Sright40.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+40)p(S+41)p(S1)='+Sright40.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+40)p(S+41)p(S2)='+Sright40.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+40)p(S+42)p(S0)='+Sright40.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+40)p(S+42)p(S1)='+Sright40.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+40)p(S+42)p(S2)='+Sright40.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+40)w(S+10)p(S0)='+Sright40.lemma+Sright10.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+40)w(S+10)p(S1)='+Sright40.lemma+Sright10.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+40)w(S+10)p(S2)='+Sright40.lemma+Sright10.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+40)w(S+11)p(S0)='+Sright40.lemma+Sright11.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+40)w(S+11)p(S1)='+Sright40.lemma+Sright11.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+40)w(S+11)p(S2)='+Sright40.lemma+Sright11.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+40)w(S+12)p(S0)='+Sright40.lemma+Sright12.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+40)w(S+12)p(S1)='+Sright40.lemma+Sright12.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+40)w(S+12)p(S2)='+Sright40.lemma+Sright12.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+40)w(S+20)p(S0)='+Sright40.lemma+Sright20.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+40)w(S+20)p(S1)='+Sright40.lemma+Sright20.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+40)w(S+20)p(S2)='+Sright40.lemma+Sright20.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+40)w(S+21)p(S0)='+Sright40.lemma+Sright21.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+40)w(S+21)p(S1)='+Sright40.lemma+Sright21.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+40)w(S+21)p(S2)='+Sright40.lemma+Sright21.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+40)w(S+22)p(S0)='+Sright40.lemma+Sright22.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+40)w(S+22)p(S1)='+Sright40.lemma+Sright22.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+40)w(S+22)p(S2)='+Sright40.lemma+Sright22.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+40)w(S+30)p(S0)='+Sright40.lemma+Sright30.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+40)w(S+30)p(S1)='+Sright40.lemma+Sright30.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+40)w(S+30)p(S2)='+Sright40.lemma+Sright30.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+40)w(S+31)p(S0)='+Sright40.lemma+Sright31.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+40)w(S+31)p(S1)='+Sright40.lemma+Sright31.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+40)w(S+31)p(S2)='+Sright40.lemma+Sright31.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+40)w(S+32)p(S0)='+Sright40.lemma+Sright32.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+40)w(S+32)p(S1)='+Sright40.lemma+Sright32.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+40)w(S+32)p(S2)='+Sright40.lemma+Sright32.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+40)w(S+40)p(S0)='+Sright40.lemma+Sright40.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+40)w(S+40)p(S1)='+Sright40.lemma+Sright40.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+40)w(S+40)p(S2)='+Sright40.lemma+Sright40.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+40)w(S+41)p(S0)='+Sright40.lemma+Sright41.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+40)w(S+41)p(S1)='+Sright40.lemma+Sright41.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+40)w(S+41)p(S2)='+Sright40.lemma+Sright41.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+40)w(S+42)p(S0)='+Sright40.lemma+Sright42.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+40)w(S+42)p(S1)='+Sright40.lemma+Sright42.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+40)w(S+42)p(S2)='+Sright40.lemma+Sright42.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+41)l(S+10)p(S0)='+Sright41.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+41)l(S+10)p(S1)='+Sright41.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+41)l(S+10)p(S2)='+Sright41.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+41)l(S+11)p(S0)='+Sright41.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+41)l(S+11)p(S1)='+Sright41.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+41)l(S+11)p(S2)='+Sright41.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+41)l(S+12)p(S0)='+Sright41.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+41)l(S+12)p(S1)='+Sright41.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+41)l(S+12)p(S2)='+Sright41.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+41)l(S+20)p(S0)='+Sright41.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+41)l(S+20)p(S1)='+Sright41.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+41)l(S+20)p(S2)='+Sright41.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+41)l(S+21)p(S0)='+Sright41.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+41)l(S+21)p(S1)='+Sright41.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+41)l(S+21)p(S2)='+Sright41.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+41)l(S+22)p(S0)='+Sright41.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+41)l(S+22)p(S1)='+Sright41.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+41)l(S+22)p(S2)='+Sright41.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+41)l(S+30)p(S0)='+Sright41.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+41)l(S+30)p(S1)='+Sright41.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+41)l(S+30)p(S2)='+Sright41.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+41)l(S+31)p(S0)='+Sright41.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+41)l(S+31)p(S1)='+Sright41.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+41)l(S+31)p(S2)='+Sright41.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+41)l(S+32)p(S0)='+Sright41.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+41)l(S+32)p(S1)='+Sright41.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+41)l(S+32)p(S2)='+Sright41.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+41)l(S+40)p(S0)='+Sright41.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+41)l(S+40)p(S1)='+Sright41.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+41)l(S+40)p(S2)='+Sright41.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+41)l(S+41)p(S0)='+Sright41.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+41)l(S+41)p(S1)='+Sright41.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+41)l(S+41)p(S2)='+Sright41.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+41)l(S+42)p(S0)='+Sright41.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+41)l(S+42)p(S1)='+Sright41.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+41)l(S+42)p(S2)='+Sright41.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+41)p(S+10)p(S0)='+Sright41.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+41)p(S+10)p(S1)='+Sright41.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+41)p(S+10)p(S2)='+Sright41.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+41)p(S+11)p(S0)='+Sright41.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+41)p(S+11)p(S1)='+Sright41.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+41)p(S+11)p(S2)='+Sright41.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+41)p(S+12)p(S0)='+Sright41.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+41)p(S+12)p(S1)='+Sright41.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+41)p(S+12)p(S2)='+Sright41.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+41)p(S+20)p(S0)='+Sright41.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+41)p(S+20)p(S1)='+Sright41.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+41)p(S+20)p(S2)='+Sright41.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+41)p(S+21)p(S0)='+Sright41.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+41)p(S+21)p(S1)='+Sright41.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+41)p(S+21)p(S2)='+Sright41.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+41)p(S+22)p(S0)='+Sright41.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+41)p(S+22)p(S1)='+Sright41.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+41)p(S+22)p(S2)='+Sright41.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+41)p(S+30)p(S0)='+Sright41.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+41)p(S+30)p(S1)='+Sright41.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+41)p(S+30)p(S2)='+Sright41.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+41)p(S+31)p(S0)='+Sright41.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+41)p(S+31)p(S1)='+Sright41.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+41)p(S+31)p(S2)='+Sright41.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+41)p(S+32)p(S0)='+Sright41.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+41)p(S+32)p(S1)='+Sright41.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+41)p(S+32)p(S2)='+Sright41.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+41)p(S+40)p(S0)='+Sright41.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+41)p(S+40)p(S1)='+Sright41.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+41)p(S+40)p(S2)='+Sright41.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+41)p(S+41)p(S0)='+Sright41.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+41)p(S+41)p(S1)='+Sright41.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+41)p(S+41)p(S2)='+Sright41.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+41)p(S+42)p(S0)='+Sright41.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+41)p(S+42)p(S1)='+Sright41.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+41)p(S+42)p(S2)='+Sright41.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+41)w(S+10)p(S0)='+Sright41.lemma+Sright10.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+41)w(S+10)p(S1)='+Sright41.lemma+Sright10.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+41)w(S+10)p(S2)='+Sright41.lemma+Sright10.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+41)w(S+11)p(S0)='+Sright41.lemma+Sright11.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+41)w(S+11)p(S1)='+Sright41.lemma+Sright11.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+41)w(S+11)p(S2)='+Sright41.lemma+Sright11.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+41)w(S+12)p(S0)='+Sright41.lemma+Sright12.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+41)w(S+12)p(S1)='+Sright41.lemma+Sright12.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+41)w(S+12)p(S2)='+Sright41.lemma+Sright12.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+41)w(S+20)p(S0)='+Sright41.lemma+Sright20.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+41)w(S+20)p(S1)='+Sright41.lemma+Sright20.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+41)w(S+20)p(S2)='+Sright41.lemma+Sright20.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+41)w(S+21)p(S0)='+Sright41.lemma+Sright21.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+41)w(S+21)p(S1)='+Sright41.lemma+Sright21.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+41)w(S+21)p(S2)='+Sright41.lemma+Sright21.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+41)w(S+22)p(S0)='+Sright41.lemma+Sright22.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+41)w(S+22)p(S1)='+Sright41.lemma+Sright22.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+41)w(S+22)p(S2)='+Sright41.lemma+Sright22.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+41)w(S+30)p(S0)='+Sright41.lemma+Sright30.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+41)w(S+30)p(S1)='+Sright41.lemma+Sright30.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+41)w(S+30)p(S2)='+Sright41.lemma+Sright30.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+41)w(S+31)p(S0)='+Sright41.lemma+Sright31.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+41)w(S+31)p(S1)='+Sright41.lemma+Sright31.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+41)w(S+31)p(S2)='+Sright41.lemma+Sright31.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+41)w(S+32)p(S0)='+Sright41.lemma+Sright32.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+41)w(S+32)p(S1)='+Sright41.lemma+Sright32.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+41)w(S+32)p(S2)='+Sright41.lemma+Sright32.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+41)w(S+40)p(S0)='+Sright41.lemma+Sright40.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+41)w(S+40)p(S1)='+Sright41.lemma+Sright40.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+41)w(S+40)p(S2)='+Sright41.lemma+Sright40.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+41)w(S+41)p(S0)='+Sright41.lemma+Sright41.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+41)w(S+41)p(S1)='+Sright41.lemma+Sright41.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+41)w(S+41)p(S2)='+Sright41.lemma+Sright41.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+41)w(S+42)p(S0)='+Sright41.lemma+Sright42.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+41)w(S+42)p(S1)='+Sright41.lemma+Sright42.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+41)w(S+42)p(S2)='+Sright41.lemma+Sright42.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+42)l(S+10)p(S0)='+Sright42.lemma+Sright10.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+42)l(S+10)p(S1)='+Sright42.lemma+Sright10.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+42)l(S+10)p(S2)='+Sright42.lemma+Sright10.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+42)l(S+11)p(S0)='+Sright42.lemma+Sright11.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+42)l(S+11)p(S1)='+Sright42.lemma+Sright11.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+42)l(S+11)p(S2)='+Sright42.lemma+Sright11.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+42)l(S+12)p(S0)='+Sright42.lemma+Sright12.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+42)l(S+12)p(S1)='+Sright42.lemma+Sright12.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+42)l(S+12)p(S2)='+Sright42.lemma+Sright12.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+42)l(S+20)p(S0)='+Sright42.lemma+Sright20.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+42)l(S+20)p(S1)='+Sright42.lemma+Sright20.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+42)l(S+20)p(S2)='+Sright42.lemma+Sright20.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+42)l(S+21)p(S0)='+Sright42.lemma+Sright21.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+42)l(S+21)p(S1)='+Sright42.lemma+Sright21.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+42)l(S+21)p(S2)='+Sright42.lemma+Sright21.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+42)l(S+22)p(S0)='+Sright42.lemma+Sright22.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+42)l(S+22)p(S1)='+Sright42.lemma+Sright22.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+42)l(S+22)p(S2)='+Sright42.lemma+Sright22.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+42)l(S+30)p(S0)='+Sright42.lemma+Sright30.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+42)l(S+30)p(S1)='+Sright42.lemma+Sright30.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+42)l(S+30)p(S2)='+Sright42.lemma+Sright30.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+42)l(S+31)p(S0)='+Sright42.lemma+Sright31.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+42)l(S+31)p(S1)='+Sright42.lemma+Sright31.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+42)l(S+31)p(S2)='+Sright42.lemma+Sright31.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+42)l(S+32)p(S0)='+Sright42.lemma+Sright32.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+42)l(S+32)p(S1)='+Sright42.lemma+Sright32.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+42)l(S+32)p(S2)='+Sright42.lemma+Sright32.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+42)l(S+40)p(S0)='+Sright42.lemma+Sright40.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+42)l(S+40)p(S1)='+Sright42.lemma+Sright40.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+42)l(S+40)p(S2)='+Sright42.lemma+Sright40.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+42)l(S+41)p(S0)='+Sright42.lemma+Sright41.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+42)l(S+41)p(S1)='+Sright42.lemma+Sright41.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+42)l(S+41)p(S2)='+Sright42.lemma+Sright41.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+42)l(S+42)p(S0)='+Sright42.lemma+Sright42.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+42)l(S+42)p(S1)='+Sright42.lemma+Sright42.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+42)l(S+42)p(S2)='+Sright42.lemma+Sright42.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+42)p(S+10)p(S0)='+Sright42.lemma+Sright10.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+42)p(S+10)p(S1)='+Sright42.lemma+Sright10.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+42)p(S+10)p(S2)='+Sright42.lemma+Sright10.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+42)p(S+11)p(S0)='+Sright42.lemma+Sright11.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+42)p(S+11)p(S1)='+Sright42.lemma+Sright11.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+42)p(S+11)p(S2)='+Sright42.lemma+Sright11.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+42)p(S+12)p(S0)='+Sright42.lemma+Sright12.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+42)p(S+12)p(S1)='+Sright42.lemma+Sright12.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+42)p(S+12)p(S2)='+Sright42.lemma+Sright12.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+42)p(S+20)p(S0)='+Sright42.lemma+Sright20.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+42)p(S+20)p(S1)='+Sright42.lemma+Sright20.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+42)p(S+20)p(S2)='+Sright42.lemma+Sright20.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+42)p(S+21)p(S0)='+Sright42.lemma+Sright21.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+42)p(S+21)p(S1)='+Sright42.lemma+Sright21.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+42)p(S+21)p(S2)='+Sright42.lemma+Sright21.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+42)p(S+22)p(S0)='+Sright42.lemma+Sright22.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+42)p(S+22)p(S1)='+Sright42.lemma+Sright22.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+42)p(S+22)p(S2)='+Sright42.lemma+Sright22.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+42)p(S+30)p(S0)='+Sright42.lemma+Sright30.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+42)p(S+30)p(S1)='+Sright42.lemma+Sright30.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+42)p(S+30)p(S2)='+Sright42.lemma+Sright30.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+42)p(S+31)p(S0)='+Sright42.lemma+Sright31.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+42)p(S+31)p(S1)='+Sright42.lemma+Sright31.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+42)p(S+31)p(S2)='+Sright42.lemma+Sright31.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+42)p(S+32)p(S0)='+Sright42.lemma+Sright32.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+42)p(S+32)p(S1)='+Sright42.lemma+Sright32.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+42)p(S+32)p(S2)='+Sright42.lemma+Sright32.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+42)p(S+40)p(S0)='+Sright42.lemma+Sright40.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+42)p(S+40)p(S1)='+Sright42.lemma+Sright40.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+42)p(S+40)p(S2)='+Sright42.lemma+Sright40.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+42)p(S+41)p(S0)='+Sright42.lemma+Sright41.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+42)p(S+41)p(S1)='+Sright42.lemma+Sright41.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+42)p(S+41)p(S2)='+Sright42.lemma+Sright41.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+42)p(S+42)p(S0)='+Sright42.lemma+Sright42.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+42)p(S+42)p(S1)='+Sright42.lemma+Sright42.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+42)p(S+42)p(S2)='+Sright42.lemma+Sright42.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['l(S+42)w(S+10)p(S0)='+Sright42.lemma+Sright10.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['l(S+42)w(S+10)p(S1)='+Sright42.lemma+Sright10.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['l(S+42)w(S+10)p(S2)='+Sright42.lemma+Sright10.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['l(S+42)w(S+11)p(S0)='+Sright42.lemma+Sright11.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['l(S+42)w(S+11)p(S1)='+Sright42.lemma+Sright11.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['l(S+42)w(S+11)p(S2)='+Sright42.lemma+Sright11.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['l(S+42)w(S+12)p(S0)='+Sright42.lemma+Sright12.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['l(S+42)w(S+12)p(S1)='+Sright42.lemma+Sright12.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['l(S+42)w(S+12)p(S2)='+Sright42.lemma+Sright12.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['l(S+42)w(S+20)p(S0)='+Sright42.lemma+Sright20.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['l(S+42)w(S+20)p(S1)='+Sright42.lemma+Sright20.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['l(S+42)w(S+20)p(S2)='+Sright42.lemma+Sright20.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['l(S+42)w(S+21)p(S0)='+Sright42.lemma+Sright21.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['l(S+42)w(S+21)p(S1)='+Sright42.lemma+Sright21.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['l(S+42)w(S+21)p(S2)='+Sright42.lemma+Sright21.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['l(S+42)w(S+22)p(S0)='+Sright42.lemma+Sright22.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['l(S+42)w(S+22)p(S1)='+Sright42.lemma+Sright22.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['l(S+42)w(S+22)p(S2)='+Sright42.lemma+Sright22.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['l(S+42)w(S+30)p(S0)='+Sright42.lemma+Sright30.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['l(S+42)w(S+30)p(S1)='+Sright42.lemma+Sright30.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['l(S+42)w(S+30)p(S2)='+Sright42.lemma+Sright30.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['l(S+42)w(S+31)p(S0)='+Sright42.lemma+Sright31.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['l(S+42)w(S+31)p(S1)='+Sright42.lemma+Sright31.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['l(S+42)w(S+31)p(S2)='+Sright42.lemma+Sright31.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['l(S+42)w(S+32)p(S0)='+Sright42.lemma+Sright32.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['l(S+42)w(S+32)p(S1)='+Sright42.lemma+Sright32.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['l(S+42)w(S+32)p(S2)='+Sright42.lemma+Sright32.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['l(S+42)w(S+40)p(S0)='+Sright42.lemma+Sright40.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['l(S+42)w(S+40)p(S1)='+Sright42.lemma+Sright40.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['l(S+42)w(S+40)p(S2)='+Sright42.lemma+Sright40.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['l(S+42)w(S+41)p(S0)='+Sright42.lemma+Sright41.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['l(S+42)w(S+41)p(S1)='+Sright42.lemma+Sright41.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['l(S+42)w(S+41)p(S2)='+Sright42.lemma+Sright41.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['l(S+42)w(S+42)p(S0)='+Sright42.lemma+Sright42.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['l(S+42)w(S+42)p(S1)='+Sright42.lemma+Sright42.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['l(S+42)w(S+42)p(S2)='+Sright42.lemma+Sright42.text+S2.pos]=1.0
    if (S0 is not None) :
        features['l(S0)='+S0.lemma]=1.0
    if (S0 is not None) and (S0 is not None) :
        features['l(S0)p(S0)='+S0.lemma+S0.pos]=1.0
    if (S0 is not None) and (S1 is not None) :
        features['l(S0)p(S1)='+S0.lemma+S1.pos]=1.0
    if (S0 is not None) and (S2 is not None) :
        features['l(S0)p(S2)='+S0.lemma+S2.pos]=1.0
    if (S1 is not None) :
        features['l(S1)='+S1.lemma]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['l(S1)p(S0)='+S1.lemma+S0.pos]=1.0
    if (S1 is not None) and (S1 is not None) :
        features['l(S1)p(S1)='+S1.lemma+S1.pos]=1.0
    if (S1 is not None) and (S2 is not None) :
        features['l(S1)p(S2)='+S1.lemma+S2.pos]=1.0
    if (S2 is not None) :
        features['l(S2)='+S2.lemma]=1.0
    if (S2 is not None) and (S0 is not None) :
        features['l(S2)p(S0)='+S2.lemma+S0.pos]=1.0
    if (S2 is not None) and (S1 is not None) :
        features['l(S2)p(S1)='+S2.lemma+S1.pos]=1.0
    if (S2 is not None) and (S2 is not None) :
        features['l(S2)p(S2)='+S2.lemma+S2.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S0 is not None) :
        features['l(ld(S0))p(S0)p(S0)='+ld_S0_.lemma+S0.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S1 is not None) :
        features['l(ld(S0))p(S0)p(S1)='+ld_S0_.lemma+S0.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S2 is not None) :
        features['l(ld(S0))p(S0)p(S2)='+ld_S0_.lemma+S0.pos+S2.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S0 is not None) :
        features['l(ld(S0))p(S1)p(S0)='+ld_S0_.lemma+S1.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S1 is not None) :
        features['l(ld(S0))p(S1)p(S1)='+ld_S0_.lemma+S1.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S2 is not None) :
        features['l(ld(S0))p(S1)p(S2)='+ld_S0_.lemma+S1.pos+S2.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S0 is not None) :
        features['l(ld(S0))p(S2)p(S0)='+ld_S0_.lemma+S2.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S1 is not None) :
        features['l(ld(S0))p(S2)p(S1)='+ld_S0_.lemma+S2.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S2 is not None) :
        features['l(ld(S0))p(S2)p(S2)='+ld_S0_.lemma+S2.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S0 is not None) :
        features['l(ld(S1))p(S0)p(S0)='+ld_S1_.lemma+S0.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S1 is not None) :
        features['l(ld(S1))p(S0)p(S1)='+ld_S1_.lemma+S0.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S2 is not None) :
        features['l(ld(S1))p(S0)p(S2)='+ld_S1_.lemma+S0.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S0 is not None) :
        features['l(ld(S1))p(S1)p(S0)='+ld_S1_.lemma+S1.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S1 is not None) :
        features['l(ld(S1))p(S1)p(S1)='+ld_S1_.lemma+S1.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S2 is not None) :
        features['l(ld(S1))p(S1)p(S2)='+ld_S1_.lemma+S1.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S0 is not None) :
        features['l(ld(S1))p(S2)p(S0)='+ld_S1_.lemma+S2.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S1 is not None) :
        features['l(ld(S1))p(S2)p(S1)='+ld_S1_.lemma+S2.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S2 is not None) :
        features['l(ld(S1))p(S2)p(S2)='+ld_S1_.lemma+S2.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S0 is not None) :
        features['l(ld(S2))p(S0)p(S0)='+ld_S2_.lemma+S0.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S1 is not None) :
        features['l(ld(S2))p(S0)p(S1)='+ld_S2_.lemma+S0.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S2 is not None) :
        features['l(ld(S2))p(S0)p(S2)='+ld_S2_.lemma+S0.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S0 is not None) :
        features['l(ld(S2))p(S1)p(S0)='+ld_S2_.lemma+S1.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S1 is not None) :
        features['l(ld(S2))p(S1)p(S1)='+ld_S2_.lemma+S1.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S2 is not None) :
        features['l(ld(S2))p(S1)p(S2)='+ld_S2_.lemma+S1.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S0 is not None) :
        features['l(ld(S2))p(S2)p(S0)='+ld_S2_.lemma+S2.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S1 is not None) :
        features['l(ld(S2))p(S2)p(S1)='+ld_S2_.lemma+S2.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S2 is not None) :
        features['l(ld(S2))p(S2)p(S2)='+ld_S2_.lemma+S2.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S0 is not None) :
        features['l(rd(S0))p(S0)p(S0)='+rd_S0_.lemma+S0.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S1 is not None) :
        features['l(rd(S0))p(S0)p(S1)='+rd_S0_.lemma+S0.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S2 is not None) :
        features['l(rd(S0))p(S0)p(S2)='+rd_S0_.lemma+S0.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S0 is not None) :
        features['l(rd(S0))p(S1)p(S0)='+rd_S0_.lemma+S1.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S1 is not None) :
        features['l(rd(S0))p(S1)p(S1)='+rd_S0_.lemma+S1.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S2 is not None) :
        features['l(rd(S0))p(S1)p(S2)='+rd_S0_.lemma+S1.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S0 is not None) :
        features['l(rd(S0))p(S2)p(S0)='+rd_S0_.lemma+S2.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S1 is not None) :
        features['l(rd(S0))p(S2)p(S1)='+rd_S0_.lemma+S2.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S2 is not None) :
        features['l(rd(S0))p(S2)p(S2)='+rd_S0_.lemma+S2.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S0 is not None) :
        features['l(rd(S1))p(S0)p(S0)='+rd_S1_.lemma+S0.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S1 is not None) :
        features['l(rd(S1))p(S0)p(S1)='+rd_S1_.lemma+S0.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S2 is not None) :
        features['l(rd(S1))p(S0)p(S2)='+rd_S1_.lemma+S0.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S0 is not None) :
        features['l(rd(S1))p(S1)p(S0)='+rd_S1_.lemma+S1.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S1 is not None) :
        features['l(rd(S1))p(S1)p(S1)='+rd_S1_.lemma+S1.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S2 is not None) :
        features['l(rd(S1))p(S1)p(S2)='+rd_S1_.lemma+S1.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S0 is not None) :
        features['l(rd(S1))p(S2)p(S0)='+rd_S1_.lemma+S2.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S1 is not None) :
        features['l(rd(S1))p(S2)p(S1)='+rd_S1_.lemma+S2.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S2 is not None) :
        features['l(rd(S1))p(S2)p(S2)='+rd_S1_.lemma+S2.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S0 is not None) :
        features['l(rd(S2))p(S0)p(S0)='+rd_S2_.lemma+S0.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S1 is not None) :
        features['l(rd(S2))p(S0)p(S1)='+rd_S2_.lemma+S0.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S2 is not None) :
        features['l(rd(S2))p(S0)p(S2)='+rd_S2_.lemma+S0.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S0 is not None) :
        features['l(rd(S2))p(S1)p(S0)='+rd_S2_.lemma+S1.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S1 is not None) :
        features['l(rd(S2))p(S1)p(S1)='+rd_S2_.lemma+S1.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S2 is not None) :
        features['l(rd(S2))p(S1)p(S2)='+rd_S2_.lemma+S1.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S0 is not None) :
        features['l(rd(S2))p(S2)p(S0)='+rd_S2_.lemma+S2.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S1 is not None) :
        features['l(rd(S2))p(S2)p(S1)='+rd_S2_.lemma+S2.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S2 is not None) :
        features['l(rd(S2))p(S2)p(S2)='+rd_S2_.lemma+S2.pos+S2.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['p(B0)l(S0)='+B0.pos+S0.lemma]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['p(B0)l(S1)='+B0.pos+S1.lemma]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['p(B0)l(S2)='+B0.pos+S2.lemma]=1.0
    if (B0 is not None) and (B0 is not None) :
        features['p(B0)p(B0)='+B0.pos+B0.pos]=1.0
    if (B0 is not None) and (B1 is not None) :
        features['p(B0)p(B1)='+B0.pos+B1.pos]=1.0
    if (B0 is not None) and (B2 is not None) :
        features['p(B0)p(B2)='+B0.pos+B2.pos]=1.0
    if (B0 is not None) and (B3 is not None) :
        features['p(B0)p(B3)='+B0.pos+B3.pos]=1.0
    if (B0 is not None) and (B4 is not None) :
        features['p(B0)p(B4)='+B0.pos+B4.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['p(B0)p(S0)='+B0.pos+S0.pos]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['p(B0)p(S1)='+B0.pos+S1.pos]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['p(B0)p(S2)='+B0.pos+S2.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['p(B0)w(S0)='+B0.pos+S0.text]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['p(B0)w(S1)='+B0.pos+S1.text]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['p(B0)w(S2)='+B0.pos+S2.text]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['p(B1)l(S0)='+B1.pos+S0.lemma]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['p(B1)l(S1)='+B1.pos+S1.lemma]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['p(B1)l(S2)='+B1.pos+S2.lemma]=1.0
    if (B1 is not None) and (B0 is not None) :
        features['p(B1)p(B0)='+B1.pos+B0.pos]=1.0
    if (B1 is not None) and (B1 is not None) :
        features['p(B1)p(B1)='+B1.pos+B1.pos]=1.0
    if (B1 is not None) and (B2 is not None) :
        features['p(B1)p(B2)='+B1.pos+B2.pos]=1.0
    if (B1 is not None) and (B3 is not None) :
        features['p(B1)p(B3)='+B1.pos+B3.pos]=1.0
    if (B1 is not None) and (B4 is not None) :
        features['p(B1)p(B4)='+B1.pos+B4.pos]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['p(B1)p(S0)='+B1.pos+S0.pos]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['p(B1)p(S1)='+B1.pos+S1.pos]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['p(B1)p(S2)='+B1.pos+S2.pos]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['p(B1)w(S0)='+B1.pos+S0.text]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['p(B1)w(S1)='+B1.pos+S1.text]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['p(B1)w(S2)='+B1.pos+S2.text]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['p(B2)l(S0)='+B2.pos+S0.lemma]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['p(B2)l(S1)='+B2.pos+S1.lemma]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['p(B2)l(S2)='+B2.pos+S2.lemma]=1.0
    if (B2 is not None) and (B0 is not None) :
        features['p(B2)p(B0)='+B2.pos+B0.pos]=1.0
    if (B2 is not None) and (B1 is not None) :
        features['p(B2)p(B1)='+B2.pos+B1.pos]=1.0
    if (B2 is not None) and (B2 is not None) :
        features['p(B2)p(B2)='+B2.pos+B2.pos]=1.0
    if (B2 is not None) and (B3 is not None) :
        features['p(B2)p(B3)='+B2.pos+B3.pos]=1.0
    if (B2 is not None) and (B4 is not None) :
        features['p(B2)p(B4)='+B2.pos+B4.pos]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['p(B2)p(S0)='+B2.pos+S0.pos]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['p(B2)p(S1)='+B2.pos+S1.pos]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['p(B2)p(S2)='+B2.pos+S2.pos]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['p(B2)w(S0)='+B2.pos+S0.text]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['p(B2)w(S1)='+B2.pos+S1.text]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['p(B2)w(S2)='+B2.pos+S2.text]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['p(B3)l(S0)='+B3.pos+S0.lemma]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['p(B3)l(S1)='+B3.pos+S1.lemma]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['p(B3)l(S2)='+B3.pos+S2.lemma]=1.0
    if (B3 is not None) and (B0 is not None) :
        features['p(B3)p(B0)='+B3.pos+B0.pos]=1.0
    if (B3 is not None) and (B1 is not None) :
        features['p(B3)p(B1)='+B3.pos+B1.pos]=1.0
    if (B3 is not None) and (B2 is not None) :
        features['p(B3)p(B2)='+B3.pos+B2.pos]=1.0
    if (B3 is not None) and (B3 is not None) :
        features['p(B3)p(B3)='+B3.pos+B3.pos]=1.0
    if (B3 is not None) and (B4 is not None) :
        features['p(B3)p(B4)='+B3.pos+B4.pos]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['p(B3)p(S0)='+B3.pos+S0.pos]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['p(B3)p(S1)='+B3.pos+S1.pos]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['p(B3)p(S2)='+B3.pos+S2.pos]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['p(B3)w(S0)='+B3.pos+S0.text]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['p(B3)w(S1)='+B3.pos+S1.text]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['p(B3)w(S2)='+B3.pos+S2.text]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['p(B4)l(S0)='+B4.pos+S0.lemma]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['p(B4)l(S1)='+B4.pos+S1.lemma]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['p(B4)l(S2)='+B4.pos+S2.lemma]=1.0
    if (B4 is not None) and (B0 is not None) :
        features['p(B4)p(B0)='+B4.pos+B0.pos]=1.0
    if (B4 is not None) and (B1 is not None) :
        features['p(B4)p(B1)='+B4.pos+B1.pos]=1.0
    if (B4 is not None) and (B2 is not None) :
        features['p(B4)p(B2)='+B4.pos+B2.pos]=1.0
    if (B4 is not None) and (B3 is not None) :
        features['p(B4)p(B3)='+B4.pos+B3.pos]=1.0
    if (B4 is not None) and (B4 is not None) :
        features['p(B4)p(B4)='+B4.pos+B4.pos]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['p(B4)p(S0)='+B4.pos+S0.pos]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['p(B4)p(S1)='+B4.pos+S1.pos]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['p(B4)p(S2)='+B4.pos+S2.pos]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['p(B4)w(S0)='+B4.pos+S0.text]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['p(B4)w(S1)='+B4.pos+S1.text]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['p(B4)w(S2)='+B4.pos+S2.text]=1.0
    if (Sright10 is not None) :
        features['p(S+10)='+Sright10.pos]=1.0
    if (Sright11 is not None) :
        features['p(S+11)='+Sright11.pos]=1.0
    if (Sright12 is not None) :
        features['p(S+12)='+Sright12.pos]=1.0
    if (Sright20 is not None) :
        features['p(S+20)='+Sright20.pos]=1.0
    if (Sright21 is not None) :
        features['p(S+21)='+Sright21.pos]=1.0
    if (Sright22 is not None) :
        features['p(S+22)='+Sright22.pos]=1.0
    if (Sright30 is not None) :
        features['p(S+30)='+Sright30.pos]=1.0
    if (Sright31 is not None) :
        features['p(S+31)='+Sright31.pos]=1.0
    if (Sright32 is not None) :
        features['p(S+32)='+Sright32.pos]=1.0
    if (Sright40 is not None) :
        features['p(S+40)='+Sright40.pos]=1.0
    if (Sright41 is not None) :
        features['p(S+41)='+Sright41.pos]=1.0
    if (Sright42 is not None) :
        features['p(S+42)='+Sright42.pos]=1.0
    if (S0 is not None) and (d0_S0_ is not None) and (d1_S0_ is not None) and (d2_S0_ is not None) :
        features['p(S0)p(d0(S0))p(d1(S0))p(d2(S0))='+S0.pos+d0_S0_.pos+d1_S0_.pos+d2_S0_.pos]=1.0
    if (S0 is not None) and (d0_S1_ is not None) and (d1_S1_ is not None) and (d2_S1_ is not None) :
        features['p(S0)p(d0(S1))p(d1(S1))p(d2(S1))='+S0.pos+d0_S1_.pos+d1_S1_.pos+d2_S1_.pos]=1.0
    if (S0 is not None) :
        features['p(S0)='+S0.pos]=1.0
    if (S0 is not None) and (S0 is not None) :
        features['p(S0)p(S0)='+S0.pos+S0.pos]=1.0
    if (S0 is not None) and (S1 is not None) :
        features['p(S0)p(S1)='+S0.pos+S1.pos]=1.0
    if (S0 is not None) and (S2 is not None) :
        features['p(S0)p(S2)='+S0.pos+S2.pos]=1.0
    if (S1 is not None) :
        features['p(S1)='+S1.pos]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['p(S1)p(S0)='+S1.pos+S0.pos]=1.0
    if (S1 is not None) and (S1 is not None) :
        features['p(S1)p(S1)='+S1.pos+S1.pos]=1.0
    if (S1 is not None) and (S2 is not None) :
        features['p(S1)p(S2)='+S1.pos+S2.pos]=1.0
    if (S2 is not None) :
        features['p(S2)='+S2.pos]=1.0
    if (S2 is not None) and (S0 is not None) :
        features['p(S2)p(S0)='+S2.pos+S0.pos]=1.0
    if (S2 is not None) and (S1 is not None) :
        features['p(S2)p(S1)='+S2.pos+S1.pos]=1.0
    if (S2 is not None) and (S2 is not None) :
        features['p(S2)p(S2)='+S2.pos+S2.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['w(B0)l(S0)='+B0.text+S0.lemma]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['w(B0)l(S1)='+B0.text+S1.lemma]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['w(B0)l(S2)='+B0.text+S2.lemma]=1.0
    if (B0 is not None) and (B0 is not None) :
        features['w(B0)p(B0)='+B0.text+B0.pos]=1.0
    if (B0 is not None) and (B1 is not None) :
        features['w(B0)p(B1)='+B0.text+B1.pos]=1.0
    if (B0 is not None) and (B2 is not None) :
        features['w(B0)p(B2)='+B0.text+B2.pos]=1.0
    if (B0 is not None) and (B3 is not None) :
        features['w(B0)p(B3)='+B0.text+B3.pos]=1.0
    if (B0 is not None) and (B4 is not None) :
        features['w(B0)p(B4)='+B0.text+B4.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['w(B0)p(S0)='+B0.text+S0.pos]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['w(B0)p(S1)='+B0.text+S1.pos]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['w(B0)p(S2)='+B0.text+S2.pos]=1.0
    if (B0 is not None) and (S0 is not None) :
        features['w(B0)w(S0)='+B0.text+S0.text]=1.0
    if (B0 is not None) and (S1 is not None) :
        features['w(B0)w(S1)='+B0.text+S1.text]=1.0
    if (B0 is not None) and (S2 is not None) :
        features['w(B0)w(S2)='+B0.text+S2.text]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['w(B1)l(S0)='+B1.text+S0.lemma]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['w(B1)l(S1)='+B1.text+S1.lemma]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['w(B1)l(S2)='+B1.text+S2.lemma]=1.0
    if (B1 is not None) and (B0 is not None) :
        features['w(B1)p(B0)='+B1.text+B0.pos]=1.0
    if (B1 is not None) and (B1 is not None) :
        features['w(B1)p(B1)='+B1.text+B1.pos]=1.0
    if (B1 is not None) and (B2 is not None) :
        features['w(B1)p(B2)='+B1.text+B2.pos]=1.0
    if (B1 is not None) and (B3 is not None) :
        features['w(B1)p(B3)='+B1.text+B3.pos]=1.0
    if (B1 is not None) and (B4 is not None) :
        features['w(B1)p(B4)='+B1.text+B4.pos]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['w(B1)p(S0)='+B1.text+S0.pos]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['w(B1)p(S1)='+B1.text+S1.pos]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['w(B1)p(S2)='+B1.text+S2.pos]=1.0
    if (B1 is not None) and (S0 is not None) :
        features['w(B1)w(S0)='+B1.text+S0.text]=1.0
    if (B1 is not None) and (S1 is not None) :
        features['w(B1)w(S1)='+B1.text+S1.text]=1.0
    if (B1 is not None) and (S2 is not None) :
        features['w(B1)w(S2)='+B1.text+S2.text]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['w(B2)l(S0)='+B2.text+S0.lemma]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['w(B2)l(S1)='+B2.text+S1.lemma]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['w(B2)l(S2)='+B2.text+S2.lemma]=1.0
    if (B2 is not None) and (B0 is not None) :
        features['w(B2)p(B0)='+B2.text+B0.pos]=1.0
    if (B2 is not None) and (B1 is not None) :
        features['w(B2)p(B1)='+B2.text+B1.pos]=1.0
    if (B2 is not None) and (B2 is not None) :
        features['w(B2)p(B2)='+B2.text+B2.pos]=1.0
    if (B2 is not None) and (B3 is not None) :
        features['w(B2)p(B3)='+B2.text+B3.pos]=1.0
    if (B2 is not None) and (B4 is not None) :
        features['w(B2)p(B4)='+B2.text+B4.pos]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['w(B2)p(S0)='+B2.text+S0.pos]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['w(B2)p(S1)='+B2.text+S1.pos]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['w(B2)p(S2)='+B2.text+S2.pos]=1.0
    if (B2 is not None) and (S0 is not None) :
        features['w(B2)w(S0)='+B2.text+S0.text]=1.0
    if (B2 is not None) and (S1 is not None) :
        features['w(B2)w(S1)='+B2.text+S1.text]=1.0
    if (B2 is not None) and (S2 is not None) :
        features['w(B2)w(S2)='+B2.text+S2.text]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['w(B3)l(S0)='+B3.text+S0.lemma]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['w(B3)l(S1)='+B3.text+S1.lemma]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['w(B3)l(S2)='+B3.text+S2.lemma]=1.0
    if (B3 is not None) and (B0 is not None) :
        features['w(B3)p(B0)='+B3.text+B0.pos]=1.0
    if (B3 is not None) and (B1 is not None) :
        features['w(B3)p(B1)='+B3.text+B1.pos]=1.0
    if (B3 is not None) and (B2 is not None) :
        features['w(B3)p(B2)='+B3.text+B2.pos]=1.0
    if (B3 is not None) and (B3 is not None) :
        features['w(B3)p(B3)='+B3.text+B3.pos]=1.0
    if (B3 is not None) and (B4 is not None) :
        features['w(B3)p(B4)='+B3.text+B4.pos]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['w(B3)p(S0)='+B3.text+S0.pos]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['w(B3)p(S1)='+B3.text+S1.pos]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['w(B3)p(S2)='+B3.text+S2.pos]=1.0
    if (B3 is not None) and (S0 is not None) :
        features['w(B3)w(S0)='+B3.text+S0.text]=1.0
    if (B3 is not None) and (S1 is not None) :
        features['w(B3)w(S1)='+B3.text+S1.text]=1.0
    if (B3 is not None) and (S2 is not None) :
        features['w(B3)w(S2)='+B3.text+S2.text]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['w(B4)l(S0)='+B4.text+S0.lemma]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['w(B4)l(S1)='+B4.text+S1.lemma]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['w(B4)l(S2)='+B4.text+S2.lemma]=1.0
    if (B4 is not None) and (B0 is not None) :
        features['w(B4)p(B0)='+B4.text+B0.pos]=1.0
    if (B4 is not None) and (B1 is not None) :
        features['w(B4)p(B1)='+B4.text+B1.pos]=1.0
    if (B4 is not None) and (B2 is not None) :
        features['w(B4)p(B2)='+B4.text+B2.pos]=1.0
    if (B4 is not None) and (B3 is not None) :
        features['w(B4)p(B3)='+B4.text+B3.pos]=1.0
    if (B4 is not None) and (B4 is not None) :
        features['w(B4)p(B4)='+B4.text+B4.pos]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['w(B4)p(S0)='+B4.text+S0.pos]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['w(B4)p(S1)='+B4.text+S1.pos]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['w(B4)p(S2)='+B4.text+S2.pos]=1.0
    if (B4 is not None) and (S0 is not None) :
        features['w(B4)w(S0)='+B4.text+S0.text]=1.0
    if (B4 is not None) and (S1 is not None) :
        features['w(B4)w(S1)='+B4.text+S1.text]=1.0
    if (B4 is not None) and (S2 is not None) :
        features['w(B4)w(S2)='+B4.text+S2.text]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+10)l(S+10)p(S0)='+Sright10.text+Sright10.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+10)l(S+11)p(S0)='+Sright10.text+Sright11.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+10)l(S+11)p(S1)='+Sright10.text+Sright11.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+10)l(S+12)p(S0)='+Sright10.text+Sright12.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+10)l(S+12)p(S2)='+Sright10.text+Sright12.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+10)l(S+20)p(S0)='+Sright10.text+Sright20.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+10)l(S+21)p(S0)='+Sright10.text+Sright21.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+10)l(S+21)p(S1)='+Sright10.text+Sright21.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+10)l(S+22)p(S0)='+Sright10.text+Sright22.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+10)l(S+22)p(S2)='+Sright10.text+Sright22.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+10)l(S+30)p(S0)='+Sright10.text+Sright30.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+10)l(S+31)p(S0)='+Sright10.text+Sright31.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+10)l(S+31)p(S1)='+Sright10.text+Sright31.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+10)l(S+32)p(S0)='+Sright10.text+Sright32.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+10)l(S+32)p(S2)='+Sright10.text+Sright32.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+10)l(S+40)p(S0)='+Sright10.text+Sright40.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+10)l(S+41)p(S0)='+Sright10.text+Sright41.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+10)l(S+41)p(S1)='+Sright10.text+Sright41.lemma+S1.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+10)l(S+42)p(S0)='+Sright10.text+Sright42.lemma+S0.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+10)l(S+42)p(S2)='+Sright10.text+Sright42.lemma+S2.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) :
        features['w(S+10)p(S+10)='+Sright10.text+Sright10.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+10)p(S+10)p(S0)='+Sright10.text+Sright10.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) :
        features['w(S+10)p(S+11)='+Sright10.text+Sright11.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+10)p(S+11)p(S0)='+Sright10.text+Sright11.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+10)p(S+11)p(S1)='+Sright10.text+Sright11.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) :
        features['w(S+10)p(S+12)='+Sright10.text+Sright12.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+10)p(S+12)p(S0)='+Sright10.text+Sright12.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+10)p(S+12)p(S2)='+Sright10.text+Sright12.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) :
        features['w(S+10)p(S+20)='+Sright10.text+Sright20.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+10)p(S+20)p(S0)='+Sright10.text+Sright20.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) :
        features['w(S+10)p(S+21)='+Sright10.text+Sright21.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+10)p(S+21)p(S0)='+Sright10.text+Sright21.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+10)p(S+21)p(S1)='+Sright10.text+Sright21.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) :
        features['w(S+10)p(S+22)='+Sright10.text+Sright22.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+10)p(S+22)p(S0)='+Sright10.text+Sright22.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+10)p(S+22)p(S2)='+Sright10.text+Sright22.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) :
        features['w(S+10)p(S+30)='+Sright10.text+Sright30.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+10)p(S+30)p(S0)='+Sright10.text+Sright30.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) :
        features['w(S+10)p(S+31)='+Sright10.text+Sright31.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+10)p(S+31)p(S0)='+Sright10.text+Sright31.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+10)p(S+31)p(S1)='+Sright10.text+Sright31.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) :
        features['w(S+10)p(S+32)='+Sright10.text+Sright32.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+10)p(S+32)p(S0)='+Sright10.text+Sright32.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+10)p(S+32)p(S2)='+Sright10.text+Sright32.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) :
        features['w(S+10)p(S+40)='+Sright10.text+Sright40.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+10)p(S+40)p(S0)='+Sright10.text+Sright40.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) :
        features['w(S+10)p(S+41)='+Sright10.text+Sright41.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+10)p(S+41)p(S0)='+Sright10.text+Sright41.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+10)p(S+41)p(S1)='+Sright10.text+Sright41.pos+S1.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) :
        features['w(S+10)p(S+42)='+Sright10.text+Sright42.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+10)p(S+42)p(S0)='+Sright10.text+Sright42.pos+S0.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+10)p(S+42)p(S2)='+Sright10.text+Sright42.pos+S2.pos]=1.0
    if (Sright10 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+10)w(S+10)p(S0)='+Sright10.text+Sright10.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+10)w(S+11)p(S0)='+Sright10.text+Sright11.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+10)w(S+11)p(S1)='+Sright10.text+Sright11.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+10)w(S+12)p(S0)='+Sright10.text+Sright12.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+10)w(S+12)p(S2)='+Sright10.text+Sright12.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+10)w(S+20)p(S0)='+Sright10.text+Sright20.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+10)w(S+21)p(S0)='+Sright10.text+Sright21.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+10)w(S+21)p(S1)='+Sright10.text+Sright21.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+10)w(S+22)p(S0)='+Sright10.text+Sright22.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+10)w(S+22)p(S2)='+Sright10.text+Sright22.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+10)w(S+30)p(S0)='+Sright10.text+Sright30.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+10)w(S+31)p(S0)='+Sright10.text+Sright31.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+10)w(S+31)p(S1)='+Sright10.text+Sright31.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+10)w(S+32)p(S0)='+Sright10.text+Sright32.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+10)w(S+32)p(S2)='+Sright10.text+Sright32.text+S2.pos]=1.0
    if (Sright10 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+10)w(S+40)p(S0)='+Sright10.text+Sright40.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+10)w(S+41)p(S0)='+Sright10.text+Sright41.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+10)w(S+41)p(S1)='+Sright10.text+Sright41.text+S1.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+10)w(S+42)p(S0)='+Sright10.text+Sright42.text+S0.pos]=1.0
    if (Sright10 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+10)w(S+42)p(S2)='+Sright10.text+Sright42.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+11)l(S+10)p(S0)='+Sright11.text+Sright10.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+11)l(S+10)p(S1)='+Sright11.text+Sright10.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+11)l(S+11)p(S1)='+Sright11.text+Sright11.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+11)l(S+12)p(S1)='+Sright11.text+Sright12.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+11)l(S+12)p(S2)='+Sright11.text+Sright12.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+11)l(S+20)p(S0)='+Sright11.text+Sright20.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+11)l(S+20)p(S1)='+Sright11.text+Sright20.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+11)l(S+21)p(S1)='+Sright11.text+Sright21.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+11)l(S+22)p(S1)='+Sright11.text+Sright22.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+11)l(S+22)p(S2)='+Sright11.text+Sright22.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+11)l(S+30)p(S0)='+Sright11.text+Sright30.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+11)l(S+30)p(S1)='+Sright11.text+Sright30.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+11)l(S+31)p(S1)='+Sright11.text+Sright31.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+11)l(S+32)p(S1)='+Sright11.text+Sright32.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+11)l(S+32)p(S2)='+Sright11.text+Sright32.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+11)l(S+40)p(S0)='+Sright11.text+Sright40.lemma+S0.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+11)l(S+40)p(S1)='+Sright11.text+Sright40.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+11)l(S+41)p(S1)='+Sright11.text+Sright41.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+11)l(S+42)p(S1)='+Sright11.text+Sright42.lemma+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+11)l(S+42)p(S2)='+Sright11.text+Sright42.lemma+S2.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) :
        features['w(S+11)p(S+10)='+Sright11.text+Sright10.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+11)p(S+10)p(S0)='+Sright11.text+Sright10.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+11)p(S+10)p(S1)='+Sright11.text+Sright10.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) :
        features['w(S+11)p(S+11)='+Sright11.text+Sright11.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+11)p(S+11)p(S1)='+Sright11.text+Sright11.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) :
        features['w(S+11)p(S+12)='+Sright11.text+Sright12.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+11)p(S+12)p(S1)='+Sright11.text+Sright12.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+11)p(S+12)p(S2)='+Sright11.text+Sright12.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) :
        features['w(S+11)p(S+20)='+Sright11.text+Sright20.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+11)p(S+20)p(S0)='+Sright11.text+Sright20.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+11)p(S+20)p(S1)='+Sright11.text+Sright20.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) :
        features['w(S+11)p(S+21)='+Sright11.text+Sright21.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+11)p(S+21)p(S1)='+Sright11.text+Sright21.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) :
        features['w(S+11)p(S+22)='+Sright11.text+Sright22.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+11)p(S+22)p(S1)='+Sright11.text+Sright22.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+11)p(S+22)p(S2)='+Sright11.text+Sright22.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) :
        features['w(S+11)p(S+30)='+Sright11.text+Sright30.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+11)p(S+30)p(S0)='+Sright11.text+Sright30.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+11)p(S+30)p(S1)='+Sright11.text+Sright30.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) :
        features['w(S+11)p(S+31)='+Sright11.text+Sright31.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+11)p(S+31)p(S1)='+Sright11.text+Sright31.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) :
        features['w(S+11)p(S+32)='+Sright11.text+Sright32.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+11)p(S+32)p(S1)='+Sright11.text+Sright32.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+11)p(S+32)p(S2)='+Sright11.text+Sright32.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) :
        features['w(S+11)p(S+40)='+Sright11.text+Sright40.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+11)p(S+40)p(S0)='+Sright11.text+Sright40.pos+S0.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+11)p(S+40)p(S1)='+Sright11.text+Sright40.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) :
        features['w(S+11)p(S+41)='+Sright11.text+Sright41.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+11)p(S+41)p(S1)='+Sright11.text+Sright41.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) :
        features['w(S+11)p(S+42)='+Sright11.text+Sright42.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+11)p(S+42)p(S1)='+Sright11.text+Sright42.pos+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+11)p(S+42)p(S2)='+Sright11.text+Sright42.pos+S2.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+11)w(S+10)p(S0)='+Sright11.text+Sright10.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+11)w(S+10)p(S1)='+Sright11.text+Sright10.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+11)w(S+11)p(S1)='+Sright11.text+Sright11.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+11)w(S+12)p(S1)='+Sright11.text+Sright12.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+11)w(S+12)p(S2)='+Sright11.text+Sright12.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+11)w(S+20)p(S0)='+Sright11.text+Sright20.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+11)w(S+20)p(S1)='+Sright11.text+Sright20.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+11)w(S+21)p(S1)='+Sright11.text+Sright21.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+11)w(S+22)p(S1)='+Sright11.text+Sright22.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+11)w(S+22)p(S2)='+Sright11.text+Sright22.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+11)w(S+30)p(S0)='+Sright11.text+Sright30.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+11)w(S+30)p(S1)='+Sright11.text+Sright30.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+11)w(S+31)p(S1)='+Sright11.text+Sright31.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+11)w(S+32)p(S1)='+Sright11.text+Sright32.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+11)w(S+32)p(S2)='+Sright11.text+Sright32.text+S2.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+11)w(S+40)p(S0)='+Sright11.text+Sright40.text+S0.pos]=1.0
    if (Sright11 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+11)w(S+40)p(S1)='+Sright11.text+Sright40.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+11)w(S+41)p(S1)='+Sright11.text+Sright41.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+11)w(S+42)p(S1)='+Sright11.text+Sright42.text+S1.pos]=1.0
    if (Sright11 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+11)w(S+42)p(S2)='+Sright11.text+Sright42.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+12)l(S+10)p(S0)='+Sright12.text+Sright10.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+12)l(S+10)p(S2)='+Sright12.text+Sright10.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+12)l(S+11)p(S1)='+Sright12.text+Sright11.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+12)l(S+11)p(S2)='+Sright12.text+Sright11.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+12)l(S+12)p(S2)='+Sright12.text+Sright12.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+12)l(S+20)p(S0)='+Sright12.text+Sright20.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+12)l(S+20)p(S2)='+Sright12.text+Sright20.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+12)l(S+21)p(S1)='+Sright12.text+Sright21.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+12)l(S+21)p(S2)='+Sright12.text+Sright21.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+12)l(S+22)p(S2)='+Sright12.text+Sright22.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+12)l(S+30)p(S0)='+Sright12.text+Sright30.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+12)l(S+30)p(S2)='+Sright12.text+Sright30.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+12)l(S+31)p(S1)='+Sright12.text+Sright31.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+12)l(S+31)p(S2)='+Sright12.text+Sright31.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+12)l(S+32)p(S2)='+Sright12.text+Sright32.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+12)l(S+40)p(S0)='+Sright12.text+Sright40.lemma+S0.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+12)l(S+40)p(S2)='+Sright12.text+Sright40.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+12)l(S+41)p(S1)='+Sright12.text+Sright41.lemma+S1.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+12)l(S+41)p(S2)='+Sright12.text+Sright41.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+12)l(S+42)p(S2)='+Sright12.text+Sright42.lemma+S2.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) :
        features['w(S+12)p(S+10)='+Sright12.text+Sright10.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+12)p(S+10)p(S0)='+Sright12.text+Sright10.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+12)p(S+10)p(S2)='+Sright12.text+Sright10.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) :
        features['w(S+12)p(S+11)='+Sright12.text+Sright11.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+12)p(S+11)p(S1)='+Sright12.text+Sright11.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+12)p(S+11)p(S2)='+Sright12.text+Sright11.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) :
        features['w(S+12)p(S+12)='+Sright12.text+Sright12.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+12)p(S+12)p(S2)='+Sright12.text+Sright12.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) :
        features['w(S+12)p(S+20)='+Sright12.text+Sright20.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+12)p(S+20)p(S0)='+Sright12.text+Sright20.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+12)p(S+20)p(S2)='+Sright12.text+Sright20.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) :
        features['w(S+12)p(S+21)='+Sright12.text+Sright21.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+12)p(S+21)p(S1)='+Sright12.text+Sright21.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+12)p(S+21)p(S2)='+Sright12.text+Sright21.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) :
        features['w(S+12)p(S+22)='+Sright12.text+Sright22.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+12)p(S+22)p(S2)='+Sright12.text+Sright22.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) :
        features['w(S+12)p(S+30)='+Sright12.text+Sright30.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+12)p(S+30)p(S0)='+Sright12.text+Sright30.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+12)p(S+30)p(S2)='+Sright12.text+Sright30.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) :
        features['w(S+12)p(S+31)='+Sright12.text+Sright31.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+12)p(S+31)p(S1)='+Sright12.text+Sright31.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+12)p(S+31)p(S2)='+Sright12.text+Sright31.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) :
        features['w(S+12)p(S+32)='+Sright12.text+Sright32.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+12)p(S+32)p(S2)='+Sright12.text+Sright32.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) :
        features['w(S+12)p(S+40)='+Sright12.text+Sright40.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+12)p(S+40)p(S0)='+Sright12.text+Sright40.pos+S0.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+12)p(S+40)p(S2)='+Sright12.text+Sright40.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) :
        features['w(S+12)p(S+41)='+Sright12.text+Sright41.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+12)p(S+41)p(S1)='+Sright12.text+Sright41.pos+S1.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+12)p(S+41)p(S2)='+Sright12.text+Sright41.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) :
        features['w(S+12)p(S+42)='+Sright12.text+Sright42.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+12)p(S+42)p(S2)='+Sright12.text+Sright42.pos+S2.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+12)w(S+10)p(S0)='+Sright12.text+Sright10.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+12)w(S+10)p(S2)='+Sright12.text+Sright10.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+12)w(S+11)p(S1)='+Sright12.text+Sright11.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+12)w(S+11)p(S2)='+Sright12.text+Sright11.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+12)w(S+12)p(S2)='+Sright12.text+Sright12.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+12)w(S+20)p(S0)='+Sright12.text+Sright20.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+12)w(S+20)p(S2)='+Sright12.text+Sright20.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+12)w(S+21)p(S1)='+Sright12.text+Sright21.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+12)w(S+21)p(S2)='+Sright12.text+Sright21.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+12)w(S+22)p(S2)='+Sright12.text+Sright22.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+12)w(S+30)p(S0)='+Sright12.text+Sright30.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+12)w(S+30)p(S2)='+Sright12.text+Sright30.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+12)w(S+31)p(S1)='+Sright12.text+Sright31.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+12)w(S+31)p(S2)='+Sright12.text+Sright31.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+12)w(S+32)p(S2)='+Sright12.text+Sright32.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+12)w(S+40)p(S0)='+Sright12.text+Sright40.text+S0.pos]=1.0
    if (Sright12 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+12)w(S+40)p(S2)='+Sright12.text+Sright40.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+12)w(S+41)p(S1)='+Sright12.text+Sright41.text+S1.pos]=1.0
    if (Sright12 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+12)w(S+41)p(S2)='+Sright12.text+Sright41.text+S2.pos]=1.0
    if (Sright12 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+12)w(S+42)p(S2)='+Sright12.text+Sright42.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+20)l(S+10)p(S0)='+Sright20.text+Sright10.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+20)l(S+11)p(S0)='+Sright20.text+Sright11.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+20)l(S+11)p(S1)='+Sright20.text+Sright11.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+20)l(S+12)p(S0)='+Sright20.text+Sright12.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+20)l(S+12)p(S2)='+Sright20.text+Sright12.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+20)l(S+20)p(S0)='+Sright20.text+Sright20.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+20)l(S+21)p(S0)='+Sright20.text+Sright21.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+20)l(S+21)p(S1)='+Sright20.text+Sright21.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+20)l(S+22)p(S0)='+Sright20.text+Sright22.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+20)l(S+22)p(S2)='+Sright20.text+Sright22.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+20)l(S+30)p(S0)='+Sright20.text+Sright30.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+20)l(S+31)p(S0)='+Sright20.text+Sright31.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+20)l(S+31)p(S1)='+Sright20.text+Sright31.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+20)l(S+32)p(S0)='+Sright20.text+Sright32.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+20)l(S+32)p(S2)='+Sright20.text+Sright32.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+20)l(S+40)p(S0)='+Sright20.text+Sright40.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+20)l(S+41)p(S0)='+Sright20.text+Sright41.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+20)l(S+41)p(S1)='+Sright20.text+Sright41.lemma+S1.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+20)l(S+42)p(S0)='+Sright20.text+Sright42.lemma+S0.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+20)l(S+42)p(S2)='+Sright20.text+Sright42.lemma+S2.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) :
        features['w(S+20)p(S+10)='+Sright20.text+Sright10.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+20)p(S+10)p(S0)='+Sright20.text+Sright10.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) :
        features['w(S+20)p(S+11)='+Sright20.text+Sright11.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+20)p(S+11)p(S0)='+Sright20.text+Sright11.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+20)p(S+11)p(S1)='+Sright20.text+Sright11.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) :
        features['w(S+20)p(S+12)='+Sright20.text+Sright12.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+20)p(S+12)p(S0)='+Sright20.text+Sright12.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+20)p(S+12)p(S2)='+Sright20.text+Sright12.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) :
        features['w(S+20)p(S+20)='+Sright20.text+Sright20.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+20)p(S+20)p(S0)='+Sright20.text+Sright20.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) :
        features['w(S+20)p(S+21)='+Sright20.text+Sright21.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+20)p(S+21)p(S0)='+Sright20.text+Sright21.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+20)p(S+21)p(S1)='+Sright20.text+Sright21.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) :
        features['w(S+20)p(S+22)='+Sright20.text+Sright22.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+20)p(S+22)p(S0)='+Sright20.text+Sright22.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+20)p(S+22)p(S2)='+Sright20.text+Sright22.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) :
        features['w(S+20)p(S+30)='+Sright20.text+Sright30.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+20)p(S+30)p(S0)='+Sright20.text+Sright30.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) :
        features['w(S+20)p(S+31)='+Sright20.text+Sright31.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+20)p(S+31)p(S0)='+Sright20.text+Sright31.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+20)p(S+31)p(S1)='+Sright20.text+Sright31.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) :
        features['w(S+20)p(S+32)='+Sright20.text+Sright32.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+20)p(S+32)p(S0)='+Sright20.text+Sright32.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+20)p(S+32)p(S2)='+Sright20.text+Sright32.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) :
        features['w(S+20)p(S+40)='+Sright20.text+Sright40.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+20)p(S+40)p(S0)='+Sright20.text+Sright40.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) :
        features['w(S+20)p(S+41)='+Sright20.text+Sright41.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+20)p(S+41)p(S0)='+Sright20.text+Sright41.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+20)p(S+41)p(S1)='+Sright20.text+Sright41.pos+S1.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) :
        features['w(S+20)p(S+42)='+Sright20.text+Sright42.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+20)p(S+42)p(S0)='+Sright20.text+Sright42.pos+S0.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+20)p(S+42)p(S2)='+Sright20.text+Sright42.pos+S2.pos]=1.0
    if (Sright20 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+20)w(S+10)p(S0)='+Sright20.text+Sright10.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+20)w(S+11)p(S0)='+Sright20.text+Sright11.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+20)w(S+11)p(S1)='+Sright20.text+Sright11.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+20)w(S+12)p(S0)='+Sright20.text+Sright12.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+20)w(S+12)p(S2)='+Sright20.text+Sright12.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+20)w(S+20)p(S0)='+Sright20.text+Sright20.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+20)w(S+21)p(S0)='+Sright20.text+Sright21.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+20)w(S+21)p(S1)='+Sright20.text+Sright21.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+20)w(S+22)p(S0)='+Sright20.text+Sright22.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+20)w(S+22)p(S2)='+Sright20.text+Sright22.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+20)w(S+30)p(S0)='+Sright20.text+Sright30.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+20)w(S+31)p(S0)='+Sright20.text+Sright31.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+20)w(S+31)p(S1)='+Sright20.text+Sright31.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+20)w(S+32)p(S0)='+Sright20.text+Sright32.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+20)w(S+32)p(S2)='+Sright20.text+Sright32.text+S2.pos]=1.0
    if (Sright20 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+20)w(S+40)p(S0)='+Sright20.text+Sright40.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+20)w(S+41)p(S0)='+Sright20.text+Sright41.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+20)w(S+41)p(S1)='+Sright20.text+Sright41.text+S1.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+20)w(S+42)p(S0)='+Sright20.text+Sright42.text+S0.pos]=1.0
    if (Sright20 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+20)w(S+42)p(S2)='+Sright20.text+Sright42.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+21)l(S+10)p(S0)='+Sright21.text+Sright10.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+21)l(S+10)p(S1)='+Sright21.text+Sright10.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+21)l(S+11)p(S1)='+Sright21.text+Sright11.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+21)l(S+12)p(S1)='+Sright21.text+Sright12.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+21)l(S+12)p(S2)='+Sright21.text+Sright12.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+21)l(S+20)p(S0)='+Sright21.text+Sright20.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+21)l(S+20)p(S1)='+Sright21.text+Sright20.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+21)l(S+21)p(S1)='+Sright21.text+Sright21.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+21)l(S+22)p(S1)='+Sright21.text+Sright22.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+21)l(S+22)p(S2)='+Sright21.text+Sright22.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+21)l(S+30)p(S0)='+Sright21.text+Sright30.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+21)l(S+30)p(S1)='+Sright21.text+Sright30.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+21)l(S+31)p(S1)='+Sright21.text+Sright31.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+21)l(S+32)p(S1)='+Sright21.text+Sright32.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+21)l(S+32)p(S2)='+Sright21.text+Sright32.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+21)l(S+40)p(S0)='+Sright21.text+Sright40.lemma+S0.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+21)l(S+40)p(S1)='+Sright21.text+Sright40.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+21)l(S+41)p(S1)='+Sright21.text+Sright41.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+21)l(S+42)p(S1)='+Sright21.text+Sright42.lemma+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+21)l(S+42)p(S2)='+Sright21.text+Sright42.lemma+S2.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) :
        features['w(S+21)p(S+10)='+Sright21.text+Sright10.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+21)p(S+10)p(S0)='+Sright21.text+Sright10.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+21)p(S+10)p(S1)='+Sright21.text+Sright10.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) :
        features['w(S+21)p(S+11)='+Sright21.text+Sright11.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+21)p(S+11)p(S1)='+Sright21.text+Sright11.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) :
        features['w(S+21)p(S+12)='+Sright21.text+Sright12.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+21)p(S+12)p(S1)='+Sright21.text+Sright12.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+21)p(S+12)p(S2)='+Sright21.text+Sright12.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) :
        features['w(S+21)p(S+20)='+Sright21.text+Sright20.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+21)p(S+20)p(S0)='+Sright21.text+Sright20.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+21)p(S+20)p(S1)='+Sright21.text+Sright20.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) :
        features['w(S+21)p(S+21)='+Sright21.text+Sright21.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+21)p(S+21)p(S1)='+Sright21.text+Sright21.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) :
        features['w(S+21)p(S+22)='+Sright21.text+Sright22.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+21)p(S+22)p(S1)='+Sright21.text+Sright22.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+21)p(S+22)p(S2)='+Sright21.text+Sright22.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) :
        features['w(S+21)p(S+30)='+Sright21.text+Sright30.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+21)p(S+30)p(S0)='+Sright21.text+Sright30.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+21)p(S+30)p(S1)='+Sright21.text+Sright30.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) :
        features['w(S+21)p(S+31)='+Sright21.text+Sright31.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+21)p(S+31)p(S1)='+Sright21.text+Sright31.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) :
        features['w(S+21)p(S+32)='+Sright21.text+Sright32.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+21)p(S+32)p(S1)='+Sright21.text+Sright32.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+21)p(S+32)p(S2)='+Sright21.text+Sright32.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) :
        features['w(S+21)p(S+40)='+Sright21.text+Sright40.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+21)p(S+40)p(S0)='+Sright21.text+Sright40.pos+S0.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+21)p(S+40)p(S1)='+Sright21.text+Sright40.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) :
        features['w(S+21)p(S+41)='+Sright21.text+Sright41.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+21)p(S+41)p(S1)='+Sright21.text+Sright41.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) :
        features['w(S+21)p(S+42)='+Sright21.text+Sright42.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+21)p(S+42)p(S1)='+Sright21.text+Sright42.pos+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+21)p(S+42)p(S2)='+Sright21.text+Sright42.pos+S2.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+21)w(S+10)p(S0)='+Sright21.text+Sright10.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+21)w(S+10)p(S1)='+Sright21.text+Sright10.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+21)w(S+11)p(S1)='+Sright21.text+Sright11.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+21)w(S+12)p(S1)='+Sright21.text+Sright12.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+21)w(S+12)p(S2)='+Sright21.text+Sright12.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+21)w(S+20)p(S0)='+Sright21.text+Sright20.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+21)w(S+20)p(S1)='+Sright21.text+Sright20.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+21)w(S+21)p(S1)='+Sright21.text+Sright21.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+21)w(S+22)p(S1)='+Sright21.text+Sright22.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+21)w(S+22)p(S2)='+Sright21.text+Sright22.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+21)w(S+30)p(S0)='+Sright21.text+Sright30.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+21)w(S+30)p(S1)='+Sright21.text+Sright30.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+21)w(S+31)p(S1)='+Sright21.text+Sright31.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+21)w(S+32)p(S1)='+Sright21.text+Sright32.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+21)w(S+32)p(S2)='+Sright21.text+Sright32.text+S2.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+21)w(S+40)p(S0)='+Sright21.text+Sright40.text+S0.pos]=1.0
    if (Sright21 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+21)w(S+40)p(S1)='+Sright21.text+Sright40.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+21)w(S+41)p(S1)='+Sright21.text+Sright41.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+21)w(S+42)p(S1)='+Sright21.text+Sright42.text+S1.pos]=1.0
    if (Sright21 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+21)w(S+42)p(S2)='+Sright21.text+Sright42.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+22)l(S+10)p(S0)='+Sright22.text+Sright10.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+22)l(S+10)p(S2)='+Sright22.text+Sright10.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+22)l(S+11)p(S1)='+Sright22.text+Sright11.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+22)l(S+11)p(S2)='+Sright22.text+Sright11.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+22)l(S+12)p(S2)='+Sright22.text+Sright12.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+22)l(S+20)p(S0)='+Sright22.text+Sright20.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+22)l(S+20)p(S2)='+Sright22.text+Sright20.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+22)l(S+21)p(S1)='+Sright22.text+Sright21.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+22)l(S+21)p(S2)='+Sright22.text+Sright21.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+22)l(S+22)p(S2)='+Sright22.text+Sright22.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+22)l(S+30)p(S0)='+Sright22.text+Sright30.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+22)l(S+30)p(S2)='+Sright22.text+Sright30.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+22)l(S+31)p(S1)='+Sright22.text+Sright31.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+22)l(S+31)p(S2)='+Sright22.text+Sright31.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+22)l(S+32)p(S2)='+Sright22.text+Sright32.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+22)l(S+40)p(S0)='+Sright22.text+Sright40.lemma+S0.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+22)l(S+40)p(S2)='+Sright22.text+Sright40.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+22)l(S+41)p(S1)='+Sright22.text+Sright41.lemma+S1.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+22)l(S+41)p(S2)='+Sright22.text+Sright41.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+22)l(S+42)p(S2)='+Sright22.text+Sright42.lemma+S2.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) :
        features['w(S+22)p(S+10)='+Sright22.text+Sright10.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+22)p(S+10)p(S0)='+Sright22.text+Sright10.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+22)p(S+10)p(S2)='+Sright22.text+Sright10.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) :
        features['w(S+22)p(S+11)='+Sright22.text+Sright11.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+22)p(S+11)p(S1)='+Sright22.text+Sright11.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+22)p(S+11)p(S2)='+Sright22.text+Sright11.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) :
        features['w(S+22)p(S+12)='+Sright22.text+Sright12.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+22)p(S+12)p(S2)='+Sright22.text+Sright12.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) :
        features['w(S+22)p(S+20)='+Sright22.text+Sright20.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+22)p(S+20)p(S0)='+Sright22.text+Sright20.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+22)p(S+20)p(S2)='+Sright22.text+Sright20.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) :
        features['w(S+22)p(S+21)='+Sright22.text+Sright21.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+22)p(S+21)p(S1)='+Sright22.text+Sright21.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+22)p(S+21)p(S2)='+Sright22.text+Sright21.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) :
        features['w(S+22)p(S+22)='+Sright22.text+Sright22.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+22)p(S+22)p(S2)='+Sright22.text+Sright22.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) :
        features['w(S+22)p(S+30)='+Sright22.text+Sright30.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+22)p(S+30)p(S0)='+Sright22.text+Sright30.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+22)p(S+30)p(S2)='+Sright22.text+Sright30.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) :
        features['w(S+22)p(S+31)='+Sright22.text+Sright31.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+22)p(S+31)p(S1)='+Sright22.text+Sright31.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+22)p(S+31)p(S2)='+Sright22.text+Sright31.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) :
        features['w(S+22)p(S+32)='+Sright22.text+Sright32.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+22)p(S+32)p(S2)='+Sright22.text+Sright32.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) :
        features['w(S+22)p(S+40)='+Sright22.text+Sright40.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+22)p(S+40)p(S0)='+Sright22.text+Sright40.pos+S0.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+22)p(S+40)p(S2)='+Sright22.text+Sright40.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) :
        features['w(S+22)p(S+41)='+Sright22.text+Sright41.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+22)p(S+41)p(S1)='+Sright22.text+Sright41.pos+S1.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+22)p(S+41)p(S2)='+Sright22.text+Sright41.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) :
        features['w(S+22)p(S+42)='+Sright22.text+Sright42.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+22)p(S+42)p(S2)='+Sright22.text+Sright42.pos+S2.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+22)w(S+10)p(S0)='+Sright22.text+Sright10.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+22)w(S+10)p(S2)='+Sright22.text+Sright10.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+22)w(S+11)p(S1)='+Sright22.text+Sright11.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+22)w(S+11)p(S2)='+Sright22.text+Sright11.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+22)w(S+12)p(S2)='+Sright22.text+Sright12.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+22)w(S+20)p(S0)='+Sright22.text+Sright20.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+22)w(S+20)p(S2)='+Sright22.text+Sright20.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+22)w(S+21)p(S1)='+Sright22.text+Sright21.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+22)w(S+21)p(S2)='+Sright22.text+Sright21.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+22)w(S+22)p(S2)='+Sright22.text+Sright22.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+22)w(S+30)p(S0)='+Sright22.text+Sright30.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+22)w(S+30)p(S2)='+Sright22.text+Sright30.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+22)w(S+31)p(S1)='+Sright22.text+Sright31.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+22)w(S+31)p(S2)='+Sright22.text+Sright31.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+22)w(S+32)p(S2)='+Sright22.text+Sright32.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+22)w(S+40)p(S0)='+Sright22.text+Sright40.text+S0.pos]=1.0
    if (Sright22 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+22)w(S+40)p(S2)='+Sright22.text+Sright40.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+22)w(S+41)p(S1)='+Sright22.text+Sright41.text+S1.pos]=1.0
    if (Sright22 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+22)w(S+41)p(S2)='+Sright22.text+Sright41.text+S2.pos]=1.0
    if (Sright22 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+22)w(S+42)p(S2)='+Sright22.text+Sright42.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+30)l(S+10)p(S0)='+Sright30.text+Sright10.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+30)l(S+11)p(S0)='+Sright30.text+Sright11.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+30)l(S+11)p(S1)='+Sright30.text+Sright11.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+30)l(S+12)p(S0)='+Sright30.text+Sright12.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+30)l(S+12)p(S2)='+Sright30.text+Sright12.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+30)l(S+20)p(S0)='+Sright30.text+Sright20.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+30)l(S+21)p(S0)='+Sright30.text+Sright21.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+30)l(S+21)p(S1)='+Sright30.text+Sright21.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+30)l(S+22)p(S0)='+Sright30.text+Sright22.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+30)l(S+22)p(S2)='+Sright30.text+Sright22.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+30)l(S+30)p(S0)='+Sright30.text+Sright30.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+30)l(S+31)p(S0)='+Sright30.text+Sright31.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+30)l(S+31)p(S1)='+Sright30.text+Sright31.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+30)l(S+32)p(S0)='+Sright30.text+Sright32.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+30)l(S+32)p(S2)='+Sright30.text+Sright32.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+30)l(S+40)p(S0)='+Sright30.text+Sright40.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+30)l(S+41)p(S0)='+Sright30.text+Sright41.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+30)l(S+41)p(S1)='+Sright30.text+Sright41.lemma+S1.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+30)l(S+42)p(S0)='+Sright30.text+Sright42.lemma+S0.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+30)l(S+42)p(S2)='+Sright30.text+Sright42.lemma+S2.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) :
        features['w(S+30)p(S+10)='+Sright30.text+Sright10.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+30)p(S+10)p(S0)='+Sright30.text+Sright10.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) :
        features['w(S+30)p(S+11)='+Sright30.text+Sright11.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+30)p(S+11)p(S0)='+Sright30.text+Sright11.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+30)p(S+11)p(S1)='+Sright30.text+Sright11.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) :
        features['w(S+30)p(S+12)='+Sright30.text+Sright12.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+30)p(S+12)p(S0)='+Sright30.text+Sright12.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+30)p(S+12)p(S2)='+Sright30.text+Sright12.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) :
        features['w(S+30)p(S+20)='+Sright30.text+Sright20.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+30)p(S+20)p(S0)='+Sright30.text+Sright20.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) :
        features['w(S+30)p(S+21)='+Sright30.text+Sright21.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+30)p(S+21)p(S0)='+Sright30.text+Sright21.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+30)p(S+21)p(S1)='+Sright30.text+Sright21.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) :
        features['w(S+30)p(S+22)='+Sright30.text+Sright22.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+30)p(S+22)p(S0)='+Sright30.text+Sright22.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+30)p(S+22)p(S2)='+Sright30.text+Sright22.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) :
        features['w(S+30)p(S+30)='+Sright30.text+Sright30.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+30)p(S+30)p(S0)='+Sright30.text+Sright30.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) :
        features['w(S+30)p(S+31)='+Sright30.text+Sright31.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+30)p(S+31)p(S0)='+Sright30.text+Sright31.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+30)p(S+31)p(S1)='+Sright30.text+Sright31.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) :
        features['w(S+30)p(S+32)='+Sright30.text+Sright32.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+30)p(S+32)p(S0)='+Sright30.text+Sright32.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+30)p(S+32)p(S2)='+Sright30.text+Sright32.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) :
        features['w(S+30)p(S+40)='+Sright30.text+Sright40.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+30)p(S+40)p(S0)='+Sright30.text+Sright40.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) :
        features['w(S+30)p(S+41)='+Sright30.text+Sright41.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+30)p(S+41)p(S0)='+Sright30.text+Sright41.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+30)p(S+41)p(S1)='+Sright30.text+Sright41.pos+S1.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) :
        features['w(S+30)p(S+42)='+Sright30.text+Sright42.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+30)p(S+42)p(S0)='+Sright30.text+Sright42.pos+S0.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+30)p(S+42)p(S2)='+Sright30.text+Sright42.pos+S2.pos]=1.0
    if (Sright30 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+30)w(S+10)p(S0)='+Sright30.text+Sright10.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+30)w(S+11)p(S0)='+Sright30.text+Sright11.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+30)w(S+11)p(S1)='+Sright30.text+Sright11.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+30)w(S+12)p(S0)='+Sright30.text+Sright12.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+30)w(S+12)p(S2)='+Sright30.text+Sright12.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+30)w(S+20)p(S0)='+Sright30.text+Sright20.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+30)w(S+21)p(S0)='+Sright30.text+Sright21.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+30)w(S+21)p(S1)='+Sright30.text+Sright21.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+30)w(S+22)p(S0)='+Sright30.text+Sright22.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+30)w(S+22)p(S2)='+Sright30.text+Sright22.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+30)w(S+30)p(S0)='+Sright30.text+Sright30.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+30)w(S+31)p(S0)='+Sright30.text+Sright31.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+30)w(S+31)p(S1)='+Sright30.text+Sright31.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+30)w(S+32)p(S0)='+Sright30.text+Sright32.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+30)w(S+32)p(S2)='+Sright30.text+Sright32.text+S2.pos]=1.0
    if (Sright30 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+30)w(S+40)p(S0)='+Sright30.text+Sright40.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+30)w(S+41)p(S0)='+Sright30.text+Sright41.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+30)w(S+41)p(S1)='+Sright30.text+Sright41.text+S1.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+30)w(S+42)p(S0)='+Sright30.text+Sright42.text+S0.pos]=1.0
    if (Sright30 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+30)w(S+42)p(S2)='+Sright30.text+Sright42.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+31)l(S+10)p(S0)='+Sright31.text+Sright10.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+31)l(S+10)p(S1)='+Sright31.text+Sright10.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+31)l(S+11)p(S1)='+Sright31.text+Sright11.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+31)l(S+12)p(S1)='+Sright31.text+Sright12.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+31)l(S+12)p(S2)='+Sright31.text+Sright12.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+31)l(S+20)p(S0)='+Sright31.text+Sright20.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+31)l(S+20)p(S1)='+Sright31.text+Sright20.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+31)l(S+21)p(S1)='+Sright31.text+Sright21.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+31)l(S+22)p(S1)='+Sright31.text+Sright22.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+31)l(S+22)p(S2)='+Sright31.text+Sright22.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+31)l(S+30)p(S0)='+Sright31.text+Sright30.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+31)l(S+30)p(S1)='+Sright31.text+Sright30.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+31)l(S+31)p(S1)='+Sright31.text+Sright31.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+31)l(S+32)p(S1)='+Sright31.text+Sright32.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+31)l(S+32)p(S2)='+Sright31.text+Sright32.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+31)l(S+40)p(S0)='+Sright31.text+Sright40.lemma+S0.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+31)l(S+40)p(S1)='+Sright31.text+Sright40.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+31)l(S+41)p(S1)='+Sright31.text+Sright41.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+31)l(S+42)p(S1)='+Sright31.text+Sright42.lemma+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+31)l(S+42)p(S2)='+Sright31.text+Sright42.lemma+S2.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) :
        features['w(S+31)p(S+10)='+Sright31.text+Sright10.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+31)p(S+10)p(S0)='+Sright31.text+Sright10.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+31)p(S+10)p(S1)='+Sright31.text+Sright10.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) :
        features['w(S+31)p(S+11)='+Sright31.text+Sright11.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+31)p(S+11)p(S1)='+Sright31.text+Sright11.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) :
        features['w(S+31)p(S+12)='+Sright31.text+Sright12.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+31)p(S+12)p(S1)='+Sright31.text+Sright12.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+31)p(S+12)p(S2)='+Sright31.text+Sright12.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) :
        features['w(S+31)p(S+20)='+Sright31.text+Sright20.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+31)p(S+20)p(S0)='+Sright31.text+Sright20.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+31)p(S+20)p(S1)='+Sright31.text+Sright20.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) :
        features['w(S+31)p(S+21)='+Sright31.text+Sright21.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+31)p(S+21)p(S1)='+Sright31.text+Sright21.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) :
        features['w(S+31)p(S+22)='+Sright31.text+Sright22.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+31)p(S+22)p(S1)='+Sright31.text+Sright22.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+31)p(S+22)p(S2)='+Sright31.text+Sright22.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) :
        features['w(S+31)p(S+30)='+Sright31.text+Sright30.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+31)p(S+30)p(S0)='+Sright31.text+Sright30.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+31)p(S+30)p(S1)='+Sright31.text+Sright30.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) :
        features['w(S+31)p(S+31)='+Sright31.text+Sright31.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+31)p(S+31)p(S1)='+Sright31.text+Sright31.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) :
        features['w(S+31)p(S+32)='+Sright31.text+Sright32.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+31)p(S+32)p(S1)='+Sright31.text+Sright32.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+31)p(S+32)p(S2)='+Sright31.text+Sright32.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) :
        features['w(S+31)p(S+40)='+Sright31.text+Sright40.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+31)p(S+40)p(S0)='+Sright31.text+Sright40.pos+S0.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+31)p(S+40)p(S1)='+Sright31.text+Sright40.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) :
        features['w(S+31)p(S+41)='+Sright31.text+Sright41.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+31)p(S+41)p(S1)='+Sright31.text+Sright41.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) :
        features['w(S+31)p(S+42)='+Sright31.text+Sright42.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+31)p(S+42)p(S1)='+Sright31.text+Sright42.pos+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+31)p(S+42)p(S2)='+Sright31.text+Sright42.pos+S2.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+31)w(S+10)p(S0)='+Sright31.text+Sright10.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+31)w(S+10)p(S1)='+Sright31.text+Sright10.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+31)w(S+11)p(S1)='+Sright31.text+Sright11.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+31)w(S+12)p(S1)='+Sright31.text+Sright12.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+31)w(S+12)p(S2)='+Sright31.text+Sright12.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+31)w(S+20)p(S0)='+Sright31.text+Sright20.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+31)w(S+20)p(S1)='+Sright31.text+Sright20.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+31)w(S+21)p(S1)='+Sright31.text+Sright21.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+31)w(S+22)p(S1)='+Sright31.text+Sright22.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+31)w(S+22)p(S2)='+Sright31.text+Sright22.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+31)w(S+30)p(S0)='+Sright31.text+Sright30.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+31)w(S+30)p(S1)='+Sright31.text+Sright30.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+31)w(S+31)p(S1)='+Sright31.text+Sright31.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+31)w(S+32)p(S1)='+Sright31.text+Sright32.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+31)w(S+32)p(S2)='+Sright31.text+Sright32.text+S2.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+31)w(S+40)p(S0)='+Sright31.text+Sright40.text+S0.pos]=1.0
    if (Sright31 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+31)w(S+40)p(S1)='+Sright31.text+Sright40.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+31)w(S+41)p(S1)='+Sright31.text+Sright41.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+31)w(S+42)p(S1)='+Sright31.text+Sright42.text+S1.pos]=1.0
    if (Sright31 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+31)w(S+42)p(S2)='+Sright31.text+Sright42.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+32)l(S+10)p(S0)='+Sright32.text+Sright10.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+32)l(S+10)p(S2)='+Sright32.text+Sright10.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+32)l(S+11)p(S1)='+Sright32.text+Sright11.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+32)l(S+11)p(S2)='+Sright32.text+Sright11.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+32)l(S+12)p(S2)='+Sright32.text+Sright12.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+32)l(S+20)p(S0)='+Sright32.text+Sright20.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+32)l(S+20)p(S2)='+Sright32.text+Sright20.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+32)l(S+21)p(S1)='+Sright32.text+Sright21.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+32)l(S+21)p(S2)='+Sright32.text+Sright21.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+32)l(S+22)p(S2)='+Sright32.text+Sright22.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+32)l(S+30)p(S0)='+Sright32.text+Sright30.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+32)l(S+30)p(S2)='+Sright32.text+Sright30.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+32)l(S+31)p(S1)='+Sright32.text+Sright31.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+32)l(S+31)p(S2)='+Sright32.text+Sright31.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+32)l(S+32)p(S2)='+Sright32.text+Sright32.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+32)l(S+40)p(S0)='+Sright32.text+Sright40.lemma+S0.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+32)l(S+40)p(S2)='+Sright32.text+Sright40.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+32)l(S+41)p(S1)='+Sright32.text+Sright41.lemma+S1.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+32)l(S+41)p(S2)='+Sright32.text+Sright41.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+32)l(S+42)p(S2)='+Sright32.text+Sright42.lemma+S2.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) :
        features['w(S+32)p(S+10)='+Sright32.text+Sright10.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+32)p(S+10)p(S0)='+Sright32.text+Sright10.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+32)p(S+10)p(S2)='+Sright32.text+Sright10.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) :
        features['w(S+32)p(S+11)='+Sright32.text+Sright11.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+32)p(S+11)p(S1)='+Sright32.text+Sright11.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+32)p(S+11)p(S2)='+Sright32.text+Sright11.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) :
        features['w(S+32)p(S+12)='+Sright32.text+Sright12.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+32)p(S+12)p(S2)='+Sright32.text+Sright12.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) :
        features['w(S+32)p(S+20)='+Sright32.text+Sright20.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+32)p(S+20)p(S0)='+Sright32.text+Sright20.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+32)p(S+20)p(S2)='+Sright32.text+Sright20.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) :
        features['w(S+32)p(S+21)='+Sright32.text+Sright21.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+32)p(S+21)p(S1)='+Sright32.text+Sright21.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+32)p(S+21)p(S2)='+Sright32.text+Sright21.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) :
        features['w(S+32)p(S+22)='+Sright32.text+Sright22.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+32)p(S+22)p(S2)='+Sright32.text+Sright22.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) :
        features['w(S+32)p(S+30)='+Sright32.text+Sright30.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+32)p(S+30)p(S0)='+Sright32.text+Sright30.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+32)p(S+30)p(S2)='+Sright32.text+Sright30.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) :
        features['w(S+32)p(S+31)='+Sright32.text+Sright31.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+32)p(S+31)p(S1)='+Sright32.text+Sright31.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+32)p(S+31)p(S2)='+Sright32.text+Sright31.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) :
        features['w(S+32)p(S+32)='+Sright32.text+Sright32.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+32)p(S+32)p(S2)='+Sright32.text+Sright32.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) :
        features['w(S+32)p(S+40)='+Sright32.text+Sright40.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+32)p(S+40)p(S0)='+Sright32.text+Sright40.pos+S0.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+32)p(S+40)p(S2)='+Sright32.text+Sright40.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) :
        features['w(S+32)p(S+41)='+Sright32.text+Sright41.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+32)p(S+41)p(S1)='+Sright32.text+Sright41.pos+S1.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+32)p(S+41)p(S2)='+Sright32.text+Sright41.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) :
        features['w(S+32)p(S+42)='+Sright32.text+Sright42.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+32)p(S+42)p(S2)='+Sright32.text+Sright42.pos+S2.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+32)w(S+10)p(S0)='+Sright32.text+Sright10.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+32)w(S+10)p(S2)='+Sright32.text+Sright10.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+32)w(S+11)p(S1)='+Sright32.text+Sright11.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+32)w(S+11)p(S2)='+Sright32.text+Sright11.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+32)w(S+12)p(S2)='+Sright32.text+Sright12.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+32)w(S+20)p(S0)='+Sright32.text+Sright20.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+32)w(S+20)p(S2)='+Sright32.text+Sright20.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+32)w(S+21)p(S1)='+Sright32.text+Sright21.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+32)w(S+21)p(S2)='+Sright32.text+Sright21.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+32)w(S+22)p(S2)='+Sright32.text+Sright22.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+32)w(S+30)p(S0)='+Sright32.text+Sright30.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+32)w(S+30)p(S2)='+Sright32.text+Sright30.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+32)w(S+31)p(S1)='+Sright32.text+Sright31.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+32)w(S+31)p(S2)='+Sright32.text+Sright31.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+32)w(S+32)p(S2)='+Sright32.text+Sright32.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+32)w(S+40)p(S0)='+Sright32.text+Sright40.text+S0.pos]=1.0
    if (Sright32 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+32)w(S+40)p(S2)='+Sright32.text+Sright40.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+32)w(S+41)p(S1)='+Sright32.text+Sright41.text+S1.pos]=1.0
    if (Sright32 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+32)w(S+41)p(S2)='+Sright32.text+Sright41.text+S2.pos]=1.0
    if (Sright32 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+32)w(S+42)p(S2)='+Sright32.text+Sright42.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+40)l(S+10)p(S0)='+Sright40.text+Sright10.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+40)l(S+11)p(S0)='+Sright40.text+Sright11.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+40)l(S+11)p(S1)='+Sright40.text+Sright11.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+40)l(S+12)p(S0)='+Sright40.text+Sright12.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+40)l(S+12)p(S2)='+Sright40.text+Sright12.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+40)l(S+20)p(S0)='+Sright40.text+Sright20.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+40)l(S+21)p(S0)='+Sright40.text+Sright21.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+40)l(S+21)p(S1)='+Sright40.text+Sright21.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+40)l(S+22)p(S0)='+Sright40.text+Sright22.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+40)l(S+22)p(S2)='+Sright40.text+Sright22.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+40)l(S+30)p(S0)='+Sright40.text+Sright30.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+40)l(S+31)p(S0)='+Sright40.text+Sright31.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+40)l(S+31)p(S1)='+Sright40.text+Sright31.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+40)l(S+32)p(S0)='+Sright40.text+Sright32.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+40)l(S+32)p(S2)='+Sright40.text+Sright32.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+40)l(S+40)p(S0)='+Sright40.text+Sright40.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+40)l(S+41)p(S0)='+Sright40.text+Sright41.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+40)l(S+41)p(S1)='+Sright40.text+Sright41.lemma+S1.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+40)l(S+42)p(S0)='+Sright40.text+Sright42.lemma+S0.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+40)l(S+42)p(S2)='+Sright40.text+Sright42.lemma+S2.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) :
        features['w(S+40)p(S+10)='+Sright40.text+Sright10.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+40)p(S+10)p(S0)='+Sright40.text+Sright10.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) :
        features['w(S+40)p(S+11)='+Sright40.text+Sright11.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+40)p(S+11)p(S0)='+Sright40.text+Sright11.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+40)p(S+11)p(S1)='+Sright40.text+Sright11.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) :
        features['w(S+40)p(S+12)='+Sright40.text+Sright12.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+40)p(S+12)p(S0)='+Sright40.text+Sright12.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+40)p(S+12)p(S2)='+Sright40.text+Sright12.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) :
        features['w(S+40)p(S+20)='+Sright40.text+Sright20.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+40)p(S+20)p(S0)='+Sright40.text+Sright20.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) :
        features['w(S+40)p(S+21)='+Sright40.text+Sright21.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+40)p(S+21)p(S0)='+Sright40.text+Sright21.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+40)p(S+21)p(S1)='+Sright40.text+Sright21.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) :
        features['w(S+40)p(S+22)='+Sright40.text+Sright22.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+40)p(S+22)p(S0)='+Sright40.text+Sright22.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+40)p(S+22)p(S2)='+Sright40.text+Sright22.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) :
        features['w(S+40)p(S+30)='+Sright40.text+Sright30.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+40)p(S+30)p(S0)='+Sright40.text+Sright30.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) :
        features['w(S+40)p(S+31)='+Sright40.text+Sright31.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+40)p(S+31)p(S0)='+Sright40.text+Sright31.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+40)p(S+31)p(S1)='+Sright40.text+Sright31.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) :
        features['w(S+40)p(S+32)='+Sright40.text+Sright32.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+40)p(S+32)p(S0)='+Sright40.text+Sright32.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+40)p(S+32)p(S2)='+Sright40.text+Sright32.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) :
        features['w(S+40)p(S+40)='+Sright40.text+Sright40.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+40)p(S+40)p(S0)='+Sright40.text+Sright40.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) :
        features['w(S+40)p(S+41)='+Sright40.text+Sright41.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+40)p(S+41)p(S0)='+Sright40.text+Sright41.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+40)p(S+41)p(S1)='+Sright40.text+Sright41.pos+S1.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) :
        features['w(S+40)p(S+42)='+Sright40.text+Sright42.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+40)p(S+42)p(S0)='+Sright40.text+Sright42.pos+S0.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+40)p(S+42)p(S2)='+Sright40.text+Sright42.pos+S2.pos]=1.0
    if (Sright40 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+40)w(S+10)p(S0)='+Sright40.text+Sright10.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S0 is not None) :
        features['w(S+40)w(S+11)p(S0)='+Sright40.text+Sright11.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+40)w(S+11)p(S1)='+Sright40.text+Sright11.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S0 is not None) :
        features['w(S+40)w(S+12)p(S0)='+Sright40.text+Sright12.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+40)w(S+12)p(S2)='+Sright40.text+Sright12.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+40)w(S+20)p(S0)='+Sright40.text+Sright20.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S0 is not None) :
        features['w(S+40)w(S+21)p(S0)='+Sright40.text+Sright21.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+40)w(S+21)p(S1)='+Sright40.text+Sright21.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S0 is not None) :
        features['w(S+40)w(S+22)p(S0)='+Sright40.text+Sright22.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+40)w(S+22)p(S2)='+Sright40.text+Sright22.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+40)w(S+30)p(S0)='+Sright40.text+Sright30.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S0 is not None) :
        features['w(S+40)w(S+31)p(S0)='+Sright40.text+Sright31.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+40)w(S+31)p(S1)='+Sright40.text+Sright31.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S0 is not None) :
        features['w(S+40)w(S+32)p(S0)='+Sright40.text+Sright32.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+40)w(S+32)p(S2)='+Sright40.text+Sright32.text+S2.pos]=1.0
    if (Sright40 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+40)w(S+40)p(S0)='+Sright40.text+Sright40.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S0 is not None) :
        features['w(S+40)w(S+41)p(S0)='+Sright40.text+Sright41.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+40)w(S+41)p(S1)='+Sright40.text+Sright41.text+S1.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S0 is not None) :
        features['w(S+40)w(S+42)p(S0)='+Sright40.text+Sright42.text+S0.pos]=1.0
    if (Sright40 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+40)w(S+42)p(S2)='+Sright40.text+Sright42.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+41)l(S+10)p(S0)='+Sright41.text+Sright10.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+41)l(S+10)p(S1)='+Sright41.text+Sright10.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+41)l(S+11)p(S1)='+Sright41.text+Sright11.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+41)l(S+12)p(S1)='+Sright41.text+Sright12.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+41)l(S+12)p(S2)='+Sright41.text+Sright12.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+41)l(S+20)p(S0)='+Sright41.text+Sright20.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+41)l(S+20)p(S1)='+Sright41.text+Sright20.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+41)l(S+21)p(S1)='+Sright41.text+Sright21.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+41)l(S+22)p(S1)='+Sright41.text+Sright22.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+41)l(S+22)p(S2)='+Sright41.text+Sright22.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+41)l(S+30)p(S0)='+Sright41.text+Sright30.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+41)l(S+30)p(S1)='+Sright41.text+Sright30.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+41)l(S+31)p(S1)='+Sright41.text+Sright31.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+41)l(S+32)p(S1)='+Sright41.text+Sright32.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+41)l(S+32)p(S2)='+Sright41.text+Sright32.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+41)l(S+40)p(S0)='+Sright41.text+Sright40.lemma+S0.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+41)l(S+40)p(S1)='+Sright41.text+Sright40.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+41)l(S+41)p(S1)='+Sright41.text+Sright41.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+41)l(S+42)p(S1)='+Sright41.text+Sright42.lemma+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+41)l(S+42)p(S2)='+Sright41.text+Sright42.lemma+S2.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) :
        features['w(S+41)p(S+10)='+Sright41.text+Sright10.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+41)p(S+10)p(S0)='+Sright41.text+Sright10.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+41)p(S+10)p(S1)='+Sright41.text+Sright10.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) :
        features['w(S+41)p(S+11)='+Sright41.text+Sright11.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+41)p(S+11)p(S1)='+Sright41.text+Sright11.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) :
        features['w(S+41)p(S+12)='+Sright41.text+Sright12.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+41)p(S+12)p(S1)='+Sright41.text+Sright12.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+41)p(S+12)p(S2)='+Sright41.text+Sright12.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) :
        features['w(S+41)p(S+20)='+Sright41.text+Sright20.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+41)p(S+20)p(S0)='+Sright41.text+Sright20.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+41)p(S+20)p(S1)='+Sright41.text+Sright20.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) :
        features['w(S+41)p(S+21)='+Sright41.text+Sright21.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+41)p(S+21)p(S1)='+Sright41.text+Sright21.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) :
        features['w(S+41)p(S+22)='+Sright41.text+Sright22.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+41)p(S+22)p(S1)='+Sright41.text+Sright22.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+41)p(S+22)p(S2)='+Sright41.text+Sright22.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) :
        features['w(S+41)p(S+30)='+Sright41.text+Sright30.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+41)p(S+30)p(S0)='+Sright41.text+Sright30.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+41)p(S+30)p(S1)='+Sright41.text+Sright30.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) :
        features['w(S+41)p(S+31)='+Sright41.text+Sright31.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+41)p(S+31)p(S1)='+Sright41.text+Sright31.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) :
        features['w(S+41)p(S+32)='+Sright41.text+Sright32.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+41)p(S+32)p(S1)='+Sright41.text+Sright32.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+41)p(S+32)p(S2)='+Sright41.text+Sright32.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) :
        features['w(S+41)p(S+40)='+Sright41.text+Sright40.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+41)p(S+40)p(S0)='+Sright41.text+Sright40.pos+S0.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+41)p(S+40)p(S1)='+Sright41.text+Sright40.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) :
        features['w(S+41)p(S+41)='+Sright41.text+Sright41.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+41)p(S+41)p(S1)='+Sright41.text+Sright41.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) :
        features['w(S+41)p(S+42)='+Sright41.text+Sright42.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+41)p(S+42)p(S1)='+Sright41.text+Sright42.pos+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+41)p(S+42)p(S2)='+Sright41.text+Sright42.pos+S2.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+41)w(S+10)p(S0)='+Sright41.text+Sright10.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright10 is not None) and (S1 is not None) :
        features['w(S+41)w(S+10)p(S1)='+Sright41.text+Sright10.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+41)w(S+11)p(S1)='+Sright41.text+Sright11.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S1 is not None) :
        features['w(S+41)w(S+12)p(S1)='+Sright41.text+Sright12.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+41)w(S+12)p(S2)='+Sright41.text+Sright12.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+41)w(S+20)p(S0)='+Sright41.text+Sright20.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright20 is not None) and (S1 is not None) :
        features['w(S+41)w(S+20)p(S1)='+Sright41.text+Sright20.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+41)w(S+21)p(S1)='+Sright41.text+Sright21.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S1 is not None) :
        features['w(S+41)w(S+22)p(S1)='+Sright41.text+Sright22.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+41)w(S+22)p(S2)='+Sright41.text+Sright22.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+41)w(S+30)p(S0)='+Sright41.text+Sright30.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright30 is not None) and (S1 is not None) :
        features['w(S+41)w(S+30)p(S1)='+Sright41.text+Sright30.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+41)w(S+31)p(S1)='+Sright41.text+Sright31.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S1 is not None) :
        features['w(S+41)w(S+32)p(S1)='+Sright41.text+Sright32.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+41)w(S+32)p(S2)='+Sright41.text+Sright32.text+S2.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+41)w(S+40)p(S0)='+Sright41.text+Sright40.text+S0.pos]=1.0
    if (Sright41 is not None) and (Sright40 is not None) and (S1 is not None) :
        features['w(S+41)w(S+40)p(S1)='+Sright41.text+Sright40.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+41)w(S+41)p(S1)='+Sright41.text+Sright41.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S1 is not None) :
        features['w(S+41)w(S+42)p(S1)='+Sright41.text+Sright42.text+S1.pos]=1.0
    if (Sright41 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+41)w(S+42)p(S2)='+Sright41.text+Sright42.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+42)l(S+10)p(S0)='+Sright42.text+Sright10.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+42)l(S+10)p(S2)='+Sright42.text+Sright10.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+42)l(S+11)p(S1)='+Sright42.text+Sright11.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+42)l(S+11)p(S2)='+Sright42.text+Sright11.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+42)l(S+12)p(S2)='+Sright42.text+Sright12.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+42)l(S+20)p(S0)='+Sright42.text+Sright20.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+42)l(S+20)p(S2)='+Sright42.text+Sright20.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+42)l(S+21)p(S1)='+Sright42.text+Sright21.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+42)l(S+21)p(S2)='+Sright42.text+Sright21.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+42)l(S+22)p(S2)='+Sright42.text+Sright22.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+42)l(S+30)p(S0)='+Sright42.text+Sright30.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+42)l(S+30)p(S2)='+Sright42.text+Sright30.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+42)l(S+31)p(S1)='+Sright42.text+Sright31.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+42)l(S+31)p(S2)='+Sright42.text+Sright31.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+42)l(S+32)p(S2)='+Sright42.text+Sright32.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+42)l(S+40)p(S0)='+Sright42.text+Sright40.lemma+S0.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+42)l(S+40)p(S2)='+Sright42.text+Sright40.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+42)l(S+41)p(S1)='+Sright42.text+Sright41.lemma+S1.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+42)l(S+41)p(S2)='+Sright42.text+Sright41.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+42)l(S+42)p(S2)='+Sright42.text+Sright42.lemma+S2.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) :
        features['w(S+42)p(S+10)='+Sright42.text+Sright10.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+42)p(S+10)p(S0)='+Sright42.text+Sright10.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+42)p(S+10)p(S2)='+Sright42.text+Sright10.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) :
        features['w(S+42)p(S+11)='+Sright42.text+Sright11.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+42)p(S+11)p(S1)='+Sright42.text+Sright11.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+42)p(S+11)p(S2)='+Sright42.text+Sright11.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) :
        features['w(S+42)p(S+12)='+Sright42.text+Sright12.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+42)p(S+12)p(S2)='+Sright42.text+Sright12.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) :
        features['w(S+42)p(S+20)='+Sright42.text+Sright20.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+42)p(S+20)p(S0)='+Sright42.text+Sright20.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+42)p(S+20)p(S2)='+Sright42.text+Sright20.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) :
        features['w(S+42)p(S+21)='+Sright42.text+Sright21.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+42)p(S+21)p(S1)='+Sright42.text+Sright21.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+42)p(S+21)p(S2)='+Sright42.text+Sright21.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) :
        features['w(S+42)p(S+22)='+Sright42.text+Sright22.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+42)p(S+22)p(S2)='+Sright42.text+Sright22.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) :
        features['w(S+42)p(S+30)='+Sright42.text+Sright30.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+42)p(S+30)p(S0)='+Sright42.text+Sright30.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+42)p(S+30)p(S2)='+Sright42.text+Sright30.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) :
        features['w(S+42)p(S+31)='+Sright42.text+Sright31.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+42)p(S+31)p(S1)='+Sright42.text+Sright31.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+42)p(S+31)p(S2)='+Sright42.text+Sright31.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) :
        features['w(S+42)p(S+32)='+Sright42.text+Sright32.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+42)p(S+32)p(S2)='+Sright42.text+Sright32.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) :
        features['w(S+42)p(S+40)='+Sright42.text+Sright40.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+42)p(S+40)p(S0)='+Sright42.text+Sright40.pos+S0.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+42)p(S+40)p(S2)='+Sright42.text+Sright40.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) :
        features['w(S+42)p(S+41)='+Sright42.text+Sright41.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+42)p(S+41)p(S1)='+Sright42.text+Sright41.pos+S1.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+42)p(S+41)p(S2)='+Sright42.text+Sright41.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) :
        features['w(S+42)p(S+42)='+Sright42.text+Sright42.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+42)p(S+42)p(S2)='+Sright42.text+Sright42.pos+S2.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S0 is not None) :
        features['w(S+42)w(S+10)p(S0)='+Sright42.text+Sright10.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright10 is not None) and (S2 is not None) :
        features['w(S+42)w(S+10)p(S2)='+Sright42.text+Sright10.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S1 is not None) :
        features['w(S+42)w(S+11)p(S1)='+Sright42.text+Sright11.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright11 is not None) and (S2 is not None) :
        features['w(S+42)w(S+11)p(S2)='+Sright42.text+Sright11.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright12 is not None) and (S2 is not None) :
        features['w(S+42)w(S+12)p(S2)='+Sright42.text+Sright12.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S0 is not None) :
        features['w(S+42)w(S+20)p(S0)='+Sright42.text+Sright20.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright20 is not None) and (S2 is not None) :
        features['w(S+42)w(S+20)p(S2)='+Sright42.text+Sright20.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S1 is not None) :
        features['w(S+42)w(S+21)p(S1)='+Sright42.text+Sright21.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright21 is not None) and (S2 is not None) :
        features['w(S+42)w(S+21)p(S2)='+Sright42.text+Sright21.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright22 is not None) and (S2 is not None) :
        features['w(S+42)w(S+22)p(S2)='+Sright42.text+Sright22.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S0 is not None) :
        features['w(S+42)w(S+30)p(S0)='+Sright42.text+Sright30.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright30 is not None) and (S2 is not None) :
        features['w(S+42)w(S+30)p(S2)='+Sright42.text+Sright30.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S1 is not None) :
        features['w(S+42)w(S+31)p(S1)='+Sright42.text+Sright31.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright31 is not None) and (S2 is not None) :
        features['w(S+42)w(S+31)p(S2)='+Sright42.text+Sright31.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright32 is not None) and (S2 is not None) :
        features['w(S+42)w(S+32)p(S2)='+Sright42.text+Sright32.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S0 is not None) :
        features['w(S+42)w(S+40)p(S0)='+Sright42.text+Sright40.text+S0.pos]=1.0
    if (Sright42 is not None) and (Sright40 is not None) and (S2 is not None) :
        features['w(S+42)w(S+40)p(S2)='+Sright42.text+Sright40.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S1 is not None) :
        features['w(S+42)w(S+41)p(S1)='+Sright42.text+Sright41.text+S1.pos]=1.0
    if (Sright42 is not None) and (Sright41 is not None) and (S2 is not None) :
        features['w(S+42)w(S+41)p(S2)='+Sright42.text+Sright41.text+S2.pos]=1.0
    if (Sright42 is not None) and (Sright42 is not None) and (S2 is not None) :
        features['w(S+42)w(S+42)p(S2)='+Sright42.text+Sright42.text+S2.pos]=1.0
    if (S0 is not None) and (Sright10 is not None) and (S1 is not None) and (S0 is not None) :
        features['w(S0)w(S+10)p(S1)p(S0)='+S0.text+Sright10.text+S1.pos+S0.pos]=1.0
    if (S0 is not None) :
        features['w(S0)='+S0.text]=1.0
    if (S0 is not None) and (S0 is not None) :
        features['w(S0)p(S0)='+S0.text+S0.pos]=1.0
    if (S0 is not None) and (S1 is not None) :
        features['w(S0)p(S1)='+S0.text+S1.pos]=1.0
    if (S0 is not None) and (S2 is not None) :
        features['w(S0)p(S2)='+S0.text+S2.pos]=1.0
    if (S1 is not None) :
        features['w(S1)='+S1.text]=1.0
    if (S1 is not None) and (S0 is not None) :
        features['w(S1)p(S0)='+S1.text+S0.pos]=1.0
    if (S1 is not None) and (S1 is not None) :
        features['w(S1)p(S1)='+S1.text+S1.pos]=1.0
    if (S1 is not None) and (S2 is not None) :
        features['w(S1)p(S2)='+S1.text+S2.pos]=1.0
    if (S2 is not None) :
        features['w(S2)='+S2.text]=1.0
    if (S2 is not None) and (S0 is not None) :
        features['w(S2)p(S0)='+S2.text+S0.pos]=1.0
    if (S2 is not None) and (S1 is not None) :
        features['w(S2)p(S1)='+S2.text+S1.pos]=1.0
    if (S2 is not None) and (S2 is not None) :
        features['w(S2)p(S2)='+S2.text+S2.pos]=1.0
    if (ld_S0_ is not None) :
        features['w(ld(S0))='+ld_S0_.text]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S0 is not None) :
        features['w(ld(S0))p(S0)p(S0)='+ld_S0_.text+S0.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S1 is not None) :
        features['w(ld(S0))p(S0)p(S1)='+ld_S0_.text+S0.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S0 is not None) and (S2 is not None) :
        features['w(ld(S0))p(S0)p(S2)='+ld_S0_.text+S0.pos+S2.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S0 is not None) :
        features['w(ld(S0))p(S1)p(S0)='+ld_S0_.text+S1.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S1 is not None) :
        features['w(ld(S0))p(S1)p(S1)='+ld_S0_.text+S1.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S1 is not None) and (S2 is not None) :
        features['w(ld(S0))p(S1)p(S2)='+ld_S0_.text+S1.pos+S2.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S0 is not None) :
        features['w(ld(S0))p(S2)p(S0)='+ld_S0_.text+S2.pos+S0.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S1 is not None) :
        features['w(ld(S0))p(S2)p(S1)='+ld_S0_.text+S2.pos+S1.pos]=1.0
    if (ld_S0_ is not None) and (S2 is not None) and (S2 is not None) :
        features['w(ld(S0))p(S2)p(S2)='+ld_S0_.text+S2.pos+S2.pos]=1.0
    if (ld_S1_ is not None) :
        features['w(ld(S1))='+ld_S1_.text]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S0 is not None) :
        features['w(ld(S1))p(S0)p(S0)='+ld_S1_.text+S0.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S1 is not None) :
        features['w(ld(S1))p(S0)p(S1)='+ld_S1_.text+S0.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S0 is not None) and (S2 is not None) :
        features['w(ld(S1))p(S0)p(S2)='+ld_S1_.text+S0.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S0 is not None) :
        features['w(ld(S1))p(S1)p(S0)='+ld_S1_.text+S1.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S1 is not None) :
        features['w(ld(S1))p(S1)p(S1)='+ld_S1_.text+S1.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S1 is not None) and (S2 is not None) :
        features['w(ld(S1))p(S1)p(S2)='+ld_S1_.text+S1.pos+S2.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S0 is not None) :
        features['w(ld(S1))p(S2)p(S0)='+ld_S1_.text+S2.pos+S0.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S1 is not None) :
        features['w(ld(S1))p(S2)p(S1)='+ld_S1_.text+S2.pos+S1.pos]=1.0
    if (ld_S1_ is not None) and (S2 is not None) and (S2 is not None) :
        features['w(ld(S1))p(S2)p(S2)='+ld_S1_.text+S2.pos+S2.pos]=1.0
    if (ld_S2_ is not None) :
        features['w(ld(S2))='+ld_S2_.text]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S0 is not None) :
        features['w(ld(S2))p(S0)p(S0)='+ld_S2_.text+S0.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S1 is not None) :
        features['w(ld(S2))p(S0)p(S1)='+ld_S2_.text+S0.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S0 is not None) and (S2 is not None) :
        features['w(ld(S2))p(S0)p(S2)='+ld_S2_.text+S0.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S0 is not None) :
        features['w(ld(S2))p(S1)p(S0)='+ld_S2_.text+S1.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S1 is not None) :
        features['w(ld(S2))p(S1)p(S1)='+ld_S2_.text+S1.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S1 is not None) and (S2 is not None) :
        features['w(ld(S2))p(S1)p(S2)='+ld_S2_.text+S1.pos+S2.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S0 is not None) :
        features['w(ld(S2))p(S2)p(S0)='+ld_S2_.text+S2.pos+S0.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S1 is not None) :
        features['w(ld(S2))p(S2)p(S1)='+ld_S2_.text+S2.pos+S1.pos]=1.0
    if (ld_S2_ is not None) and (S2 is not None) and (S2 is not None) :
        features['w(ld(S2))p(S2)p(S2)='+ld_S2_.text+S2.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S0 is not None) :
        features['w(rd(S0))p(S0)p(S0)='+rd_S0_.text+S0.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S1 is not None) :
        features['w(rd(S0))p(S0)p(S1)='+rd_S0_.text+S0.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S0 is not None) and (S2 is not None) :
        features['w(rd(S0))p(S0)p(S2)='+rd_S0_.text+S0.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S0 is not None) :
        features['w(rd(S0))p(S1)p(S0)='+rd_S0_.text+S1.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S1 is not None) :
        features['w(rd(S0))p(S1)p(S1)='+rd_S0_.text+S1.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S1 is not None) and (S2 is not None) :
        features['w(rd(S0))p(S1)p(S2)='+rd_S0_.text+S1.pos+S2.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S0 is not None) :
        features['w(rd(S0))p(S2)p(S0)='+rd_S0_.text+S2.pos+S0.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S1 is not None) :
        features['w(rd(S0))p(S2)p(S1)='+rd_S0_.text+S2.pos+S1.pos]=1.0
    if (rd_S0_ is not None) and (S2 is not None) and (S2 is not None) :
        features['w(rd(S0))p(S2)p(S2)='+rd_S0_.text+S2.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S0 is not None) :
        features['w(rd(S1))p(S0)p(S0)='+rd_S1_.text+S0.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S1 is not None) :
        features['w(rd(S1))p(S0)p(S1)='+rd_S1_.text+S0.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S0 is not None) and (S2 is not None) :
        features['w(rd(S1))p(S0)p(S2)='+rd_S1_.text+S0.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S0 is not None) :
        features['w(rd(S1))p(S1)p(S0)='+rd_S1_.text+S1.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S1 is not None) :
        features['w(rd(S1))p(S1)p(S1)='+rd_S1_.text+S1.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S1 is not None) and (S2 is not None) :
        features['w(rd(S1))p(S1)p(S2)='+rd_S1_.text+S1.pos+S2.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S0 is not None) :
        features['w(rd(S1))p(S2)p(S0)='+rd_S1_.text+S2.pos+S0.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S1 is not None) :
        features['w(rd(S1))p(S2)p(S1)='+rd_S1_.text+S2.pos+S1.pos]=1.0
    if (rd_S1_ is not None) and (S2 is not None) and (S2 is not None) :
        features['w(rd(S1))p(S2)p(S2)='+rd_S1_.text+S2.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S0 is not None) :
        features['w(rd(S2))p(S0)p(S0)='+rd_S2_.text+S0.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S1 is not None) :
        features['w(rd(S2))p(S0)p(S1)='+rd_S2_.text+S0.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S0 is not None) and (S2 is not None) :
        features['w(rd(S2))p(S0)p(S2)='+rd_S2_.text+S0.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S0 is not None) :
        features['w(rd(S2))p(S1)p(S0)='+rd_S2_.text+S1.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S1 is not None) :
        features['w(rd(S2))p(S1)p(S1)='+rd_S2_.text+S1.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S1 is not None) and (S2 is not None) :
        features['w(rd(S2))p(S1)p(S2)='+rd_S2_.text+S1.pos+S2.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S0 is not None) :
        features['w(rd(S2))p(S2)p(S0)='+rd_S2_.text+S2.pos+S0.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S1 is not None) :
        features['w(rd(S2))p(S2)p(S1)='+rd_S2_.text+S2.pos+S1.pos]=1.0
    if (rd_S2_ is not None) and (S2 is not None) and (S2 is not None) :
        features['w(rd(S2))p(S2)p(S2)='+rd_S2_.text+S2.pos+S2.pos]=1.0
    return features
