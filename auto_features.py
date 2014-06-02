
def get_transitions(state):
    """ Return as many as found, max 4 (as a list) """
    transit=[]
    for trans in reversed(state.transitions):
        transit.append(trans)
        if len(transit)>4:
            return transit
    return transit

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


def create_all_features(state):
    S0,S1,S2=get_from_stack(state.stack)
    features={}
    v0=S1
    if (v0 is not None) :
        features['p(S1)='+v0.pos]=1.0
    v0=S0
    if (v0 is not None) :
        features['p(S0)='+v0.pos]=1.0
    v0=S1
    if (v0 is not None) :
        features['l(S1)='+v0.lemma]=1.0
    v0=S0
    if (v0 is not None) :
        features['l(S0)='+v0.lemma]=1.0
    v0=S1
    if (v0 is not None) :
        features['w(S1)='+v0.text]=1.0
    v0=S0
    if (v0 is not None) :
        features['w(S0)='+v0.text]=1.0
    v0=get_following(S0,'+1',state)
    if (v0 is not None) :
        features['p(S+10)='+v0.pos]=1.0
    v0=get_following(S0,'+2',state)
    if (v0 is not None) :
        features['p(S+20)='+v0.pos]=1.0
    v0=get_child(S0,'ld',state)
    if (v0 is not None) :
        features['w(ld(S0))='+v0.text]=1.0
    v0=get_child(S1,'ld',state)
    if (v0 is not None) :
        features['w(ld(S1))='+v0.text]=1.0
    v0=S1
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['w(S1)p(S0)='+v0.text+v1.pos]=1.0
    v0=S1
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['p(S1)w(S0)='+v0.pos+v1.text]=1.0
    v0=S0
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['w(S0)p(S0)='+v0.text+v1.pos]=1.0
    v0=S1
    v1=S1
    if (v0 is not None) and (v1 is not None) :
        features['w(S1)p(S1)='+v0.text+v1.pos]=1.0
    v0=S1
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['w(S1)w(S0)='+v0.text+v1.text]=1.0
    v0=S1
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['l(S1)p(S0)='+v0.lemma+v1.pos]=1.0
    v0=S1
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['p(S1)l(S0)='+v0.pos+v1.lemma]=1.0
    v0=get_following(S0,'+2',state)
    v1=get_following(S0,'+2',state)
    if (v0 is not None) and (v1 is not None) :
        features['w(S+20)p(S+20)='+v0.text+v1.pos]=1.0
    v0=S1
    v1=S0
    if (v0 is not None) and (v1 is not None) :
        features['p(S1)p(S0)='+v0.pos+v1.pos]=1.0
    v0=get_following(S0,'+1',state)
    v1=get_following(S0,'+1',state)
    if (v0 is not None) and (v1 is not None) :
        features['w(S+10)p(S+10)='+v0.text+v1.pos]=1.0
    v0=get_following(S1,'+1',state)
    v1=get_following(S0,'+2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+11)w(S+20)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+2',state)
    v1=get_following(S0,'+3',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+21)w(S+30)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+2',state)
    v1=get_following(S0,'+1',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+21)w(S+10)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+3',state)
    v1=get_following(S0,'+2',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+31)w(S+20)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+1',state)
    v1=get_following(S0,'+2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+11)w(S+20)p(S0)='+v0.pos+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+2',state)
    v1=get_following(S0,'+3',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+21)w(S+30)p(S0)='+v0.pos+v1.text+v2.pos]=1.0
    v0=get_following(S0,'+1',state)
    v1=get_following(S1,'+2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+10)p(S+21)p(S0)='+v0.text+v1.pos+v2.pos]=1.0
    v0=get_following(S0,'+2',state)
    v1=get_following(S1,'+3',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+20)p(S+31)p(S0)='+v0.text+v1.pos+v2.pos]=1.0
    v0=get_following(S1,'+1',state)
    v1=get_following(S1,'+2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+11)w(S+21)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+2',state)
    v1=get_following(S1,'+3',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+21)w(S+31)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+3',state)
    v1=get_following(S1,'+4',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+31)w(S+41)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'+1',state)
    v1=get_following(S0,'+2',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+10)w(S+20)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'+2',state)
    v1=get_following(S0,'+3',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+20)w(S+30)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'+3',state)
    v1=get_following(S0,'+4',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+30)w(S+40)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+2',state)
    v1=get_following(S1,'-1',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+21)w(S-11)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+3',state)
    v1=get_following(S1,'-1',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+31)w(S-11)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'+2',state)
    v1=get_following(S0,'-1',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+20)w(S-10)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'+3',state)
    v1=get_following(S0,'-1',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S+30)w(S-10)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'-1',state)
    v1=get_following(S1,'-2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S-11)w(S-21)p(S0)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'-2',state)
    v1=get_following(S1,'-3',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S-21)w(S-31)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'-1',state)
    v1=get_following(S0,'-2',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S-10)w(S-20)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S0,'-2',state)
    v1=get_following(S0,'-3',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S-20)w(S-30)p(S1)='+v0.text+v1.text+v2.pos]=1.0
    v0=get_following(S1,'+1',state)
    v1=get_following(S1,'+2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+11)p(S+21)p(S0)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S1,'+2',state)
    v1=get_following(S1,'+3',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+21)p(S+31)p(S0)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S1,'+3',state)
    v1=get_following(S1,'+4',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+31)p(S+41)p(S0)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S1,'-1',state)
    v1=get_following(S1,'-2',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S-11)p(S-21)p(S0)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S1,'-2',state)
    v1=get_following(S1,'-3',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S-21)p(S-31)p(S0)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S0,'+1',state)
    v1=get_following(S0,'+2',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+10)p(S+20)p(S1)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S0,'+2',state)
    v1=get_following(S0,'+3',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+20)p(S+30)p(S1)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S0,'+3',state)
    v1=get_following(S0,'+4',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S+30)p(S+40)p(S1)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S0,'-1',state)
    v1=get_following(S0,'-2',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S-10)p(S-20)p(S1)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_following(S0,'-2',state)
    v1=get_following(S0,'-3',state)
    v2=S1
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S-20)p(S-30)p(S1)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=get_child(S1,'rd',state)
    v1=S1
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['d(rd(S1))p(S1)p(S0)='+v0.dtype+v1.pos+v2.pos]=1.0
    v0=S0
    v1=S1
    v2=get_child(S1,'ld',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(S1)d(ld(S1))='+v0.pos+v1.pos+v2.dtype]=1.0
    v0=S0
    v1=S1
    v2=get_child(S1,'rd',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(S1)d(rd(S1))='+v0.pos+v1.pos+v2.dtype]=1.0
    v0=S0
    v1=S1
    v2=get_child(S1,'rd',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S0)p(S1)w(rd(S1))='+v0.text+v1.pos+v2.text]=1.0
    v0=S1
    v1=S0
    v2=get_child(S1,'rd',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S1)p(S0)w(rd(S1))='+v0.text+v1.pos+v2.text]=1.0
    v0=S0
    v1=S1
    v2=get_child(S1,'rd',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['l(S0)p(S1)l(rd(S1))='+v0.lemma+v1.pos+v2.lemma]=1.0
    v0=S1
    v1=S0
    v2=get_child(S1,'rd',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['l(S1)p(S0)l(rd(S1))='+v0.lemma+v1.pos+v2.lemma]=1.0
    v0=S0
    v1=get_child(S1,'d0',state)
    v2=get_child(S1,'d1',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(d0(S1))w(d1(S1))='+v0.pos+v1.pos+v2.text]=1.0
    v0=S0
    v1=get_child(S1,'d0',state)
    v2=get_child(S1,'d1',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(d0(S1))p(d1(S1))='+v0.pos+v1.pos+v2.pos]=1.0
    v0=S0
    v1=S1
    v2=get_child(S2,'ld',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(S1)p(ld(S2))='+v0.pos+v1.pos+v2.pos]=1.0
    v0=S0
    v1=S1
    v2=get_child(S2,'ld',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(S1)d(ld(S2))='+v0.pos+v1.pos+v2.dtype]=1.0
    v0=S0
    v1=S1
    v2=None
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(S1)p(S2)='+v0.pos+v1.pos+v2.pos]=1.0
    v0=S0
    v1=S0
    v2=get_child(S0,'rd',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['w(S0)p(S0)p(rd(S0))='+v0.text+v1.pos+v2.pos]=1.0
    v0=get_child(S0,'rd',state)
    v1=get_child(S0,'rd',state)
    v2=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(rd(S0))d(rd(S0))p(S0)='+v0.pos+v1.dtype+v2.pos]=1.0
    v0=S0
    v1=get_child(S0,'d0',state)
    v2=get_child(S0,'d1',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) :
        features['p(S0)p(d0(S0))p(d1(S0))='+v0.pos+v1.pos+v2.pos]=1.0
    v0=S0
    v1=get_following(S0,'+1',state)
    v2=S1
    v3=S0
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) :
        features['w(S0)w(S+10)p(S1)p(S0)='+v0.text+v1.text+v2.pos+v3.pos]=1.0
    v0=S0
    v1=get_child(S0,'d0',state)
    v2=get_child(S0,'d1',state)
    v3=get_child(S0,'d2',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) :
        features['p(S0)p(d0(S0))p(d1(S0))p(d2(S0))='+v0.pos+v1.pos+v2.pos+v3.pos]=1.0
    v0=S0
    v1=get_child(S0,'d0',state)
    v2=get_child(S0,'d1',state)
    v3=get_child(S0,'d2',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) :
        features['p(S0)d(d0(S0))d(d1(S0))d(d2(S0))='+v0.pos+v1.dtype+v2.dtype+v3.dtype]=1.0
    v0=S0
    v1=get_child(S1,'d0',state)
    v2=get_child(S1,'d1',state)
    v3=get_child(S1,'d2',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) :
        features['p(S0)p(d0(S1))p(d1(S1))p(d2(S1))='+v0.pos+v1.pos+v2.pos+v3.pos]=1.0
    v0=S0
    v1=get_child(S1,'d0',state)
    v2=get_child(S1,'d1',state)
    v3=get_child(S1,'d2',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) :
        features['p(S0)d(d0(S1))d(d1(S1))d(d2(S1))='+v0.pos+v1.dtype+v2.dtype+v3.dtype]=1.0
    v0=S0
    v1=S0
    v2=get_child(S0,'d0',state)
    v3=get_child(S0,'d1',state)
    v4=get_child(S0,'d2',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) and (v4 is not None) :
        features['p(S0)l(S0)d(d0(S0))d(d1(S0))d(d2(S0))='+v0.pos+v1.lemma+v2.dtype+v3.dtype+v4.dtype]=1.0
    v0=S0
    v1=S0
    v2=get_child(S1,'d0',state)
    v3=get_child(S1,'d1',state)
    v4=get_child(S1,'d2',state)
    if (v0 is not None) and (v1 is not None) and (v2 is not None) and (v3 is not None) and (v4 is not None) :
        features['p(S0)l(S0)d(d0(S1))d(d1(S1))d(d2(S1))='+v0.pos+v1.lemma+v2.dtype+v3.dtype+v4.dtype]=1.0

    ### manually added features ###
    if (S0 is not None) and (S1 is not None): # all of these needs S0 and S1, so check these first
        for i in xrange(1,4):
            for char in ['+','-']:
                idx=char+str(i)
                v0=get_following(S0,idx,state)
                if v0 is not None:
                    features['p(S1)p(S0)p(S'+idx+'0)='+S1.pos+S0.pos+v0.pos]=1.0
                v0=get_following(S1,idx,state)
                if v0 is not None:
                    features['p(S1)p(S0)p(S'+idx+'1)='+S1.pos+S0.pos+v0.pos]=1.0
        for idx_1 in ['-1','+1']:
            for idx_0 in ['-1','+1']:
                v0=get_following(S1,idx_1,state)
                v1=get_following(S0,idx_0,state)
                if (v0 is not None) and (v1 is not None):
                    features['p(S'+idx_1+'1)p(S'+idx_0+'0)w(S0)='+v0.pos+v1.pos+S0.text]=1.0
                    features['p(S1)p(S0)p(S'+idx_1+'1)p(S'+idx_0+'0)='+S1.pos+S0.pos+v0.pos+v1.pos]=1.0
        for idx_1 in ['-2','+2']:
            for idx_0 in ['-2','+2']:
                v0=get_following(S1,idx_1,state)
                v1=get_following(S0,idx_0,state)
                if (v0 is not None) and (v1 is not None):
                    features['p(S1)p(S0)p(S'+idx_1+'1)p(S'+idx_0+'0)='+S1.pos+S0.pos+v0.pos+v1.pos]=1.0

        # morpho
        tags0=S0.feat.split(u"|")
        tags1=S1.feat.split(u"|")
        for i in xrange(0,len(tags0)):
            features['p(S0)p(S1)m(S0)='+S0.pos+S1.pos+tags0[i]]=1.0
        for i in xrange(0,len(tags1)):
            features['p(S0)p(S1)m(S1)='+S0.pos+S1.pos+tags1[i]]=1.0
        for i in xrange(0,len(tags0)):
            for j in xrange(0,len(tags1)):
                features['p(S0)p(S1)m(S0)m(S1)='+S0.pos+S1.pos+tags0[i]+tags1[j]]=1.0

    if S0 is not None:
        transit=get_transitions(state)
        if transit:
            for i in xrange(0,len(transit)):
                name='p(S0)h'+'h'.join(str(j) for j in xrange(0,i+1)) # feature name
                value=S0.pos+''.join(str(t.move)+str(t.dType) for t in transit[:i+1]) # feature 'value'
                features[name+'='+value]=1.0


    return features
