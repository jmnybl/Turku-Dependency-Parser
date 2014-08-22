
def get_following(token,idx,state):
    if token is None: return None
    if idx[0]==u"+":
        index=token.index+int(idx[1])
    elif idx[0]==u"-":
        index=token.index-int(idx[1])
    else: return None
    if index<0 or index>len(state.tree.tokens)-1: return None
    return state.tree.tokens[index]


def create_first_order(p,d,order,state):
    features={}
    pright1 = get_following(p,'+1',state)
    dright1 = get_following(d,'+1',state)
    dleft1 = get_following(d,'-1',state)
    pleft1 = get_following(p,'-1',state)
    pright2 = get_following(p,'+2',state)
    dright2 = get_following(d,'+2',state)
    dleft2 = get_following(d,'-2',state)
    pleft2 = get_following(p,'-2',state)
    features['w(p)p(d)o(d,p)='+p.text+d.pos+"_"+str(order)]=1.0
    features['w(p)o(d,p)='+p.text+"_"+str(order)]=1.0
    features['w(d)p(p)o(d,p)='+d.text+p.pos+"_"+str(order)]=1.0
    features['w(d)o(d,p)='+d.text+"_"+str(order)]=1.0
    features['w(p)w(d)o(d,p)='+p.text+d.text+"_"+str(order)]=1.0
    features['p(d)o(d,p)='+d.pos+"_"+str(order)]=1.0
    features['p(p)o(d,p)='+p.pos+"_"+str(order)]=1.0
    features['p(p)p(d)o(d,p)='+p.pos+d.pos+"_"+str(order)]=1.0
    if (pright1 is not None) and (dright1 is not None) :
        loc=order
        if p.index+1==d.index: loc+=4
        elif p.index==d.index+1: loc+=5
        else: loc+=6
        features['p(p)p(p+1)p(d)p(d+1)o(d,p)='+p.pos+pright1.pos+d.pos+dright1.pos+"_"+str(loc)]=1.0
    if (dleft1 is not None) and (pright1 is not None) :
        loc=order
        if p.index+1==d.index: loc+=4
        elif p.index==d.index-1: loc+=5
        else: loc+=6
        features['p(p)p(p+1)p(d)p(d-1)o(d,p)='+p.pos+pright1.pos+d.pos+dleft1.pos+"_"+str(loc)]=1.0
    if (dleft1 is not None) and (pleft1 is not None) :
        loc=order
        if p.index-1==d.index: loc+=4
        elif p.index==d.index-1: loc+=5
        else: loc+=6
        features['p(p)p(p-1)p(d)p(d-1)o(d,p)='+p.pos+pleft1.pos+d.pos+dleft1.pos+"_"+str(loc)]=1.0
    if (pleft1 is not None) and (dright1 is not None) :
        loc=order
        if p.index-1==d.index: loc+=4
        elif p.index==d.index+1: loc+=5
        else: loc+=6
        features['p(p)p(p-1)p(d)p(d+1)o(d,p)='+p.pos+pleft1.pos+d.pos+dright1.pos+"_"+str(loc)]=1.0
    if (pleft1 is not None) :
        loc=order
        if p.index-1==d.index: loc+=4
        else: loc+=5
        features['p(p)p(p-1)p(d)o(d,p)='+p.pos+pleft1.pos+d.pos+"_"+str(loc)]=1.0
    if (dleft1 is not None) :
        loc=order
        if p.index==d.index-1: loc+=4
        else: loc+=5
        features['p(p)p(d-1)p(d)o(d,p)='+p.pos+dleft1.pos+d.pos+"_"+str(loc)]=1.0
    if (dright1 is not None) :
        loc=order
        if p.index==d.index+1: loc+=4
        else: loc+=5
        features['p(p)p(d+1)p(d)o(d,p)='+p.pos+dright1.pos+d.pos+"_"+str(loc)]=1.0
    if (pright1 is not None) :
        loc=order
        if p.index+1==d.index: loc+=4
        else: loc+=5
        features['p(p)p(p+1)p(d)o(d,p)='+p.pos+pright1.pos+d.pos+"_"+str(loc)]=1.0
    if (pright2 is not None) and (dright2 is not None) :
        loc=order
        if p.index+2==d.index: loc+=4
        elif p.index==d.index+2: loc+=5
        else: loc+=6
        features['p(p)p(p+2)p(d)p(d+2)o(d,p)='+p.pos+pright2.pos+d.pos+dright2.pos+"_"+str(loc)]=1.0
    if (pright2 is not None) and (dleft2 is not None) :
        loc=order
        if p.index+2==d.index: loc+=4
        elif p.index==d.index-2: loc+=5
        else: loc+=6
        features['p(p)p(p+2)p(d)p(d-2)o(d,p)='+p.pos+pright2.pos+d.pos+dleft2.pos+"_"+str(loc)]=1.0
    if (dleft2 is not None) and (pleft2 is not None) :
        loc=order
        if p.index-2==d.index: loc+=4
        elif p.index==d.index-2: loc+=5
        else: loc+=6
        features['p(p)p(p-2)p(d)p(d-2)o(d,p)='+p.pos+pleft2.pos+d.pos+dleft2.pos+"_"+str(loc)]=1.0
    if (dright2 is not None) and (pleft2 is not None) :
        loc=order
        if p.index-2==d.index: loc+=4
        elif p.index==d.index+2: loc+=5
        else: loc+=6
        features['p(p)p(p-2)p(d)p(d+2)o(d,p)='+p.pos+pleft2.pos+d.pos+dright2.pos+"_"+str(loc)]=1.0
    if (pleft2 is not None) :
        loc=order
        if p.index-2==d.index: loc+=4
        else: loc+=5
        features['p(p)p(p-2)p(d)o(d,p)='+p.pos+pleft2.pos+d.pos+"_"+str(loc)]=1.0
    if (dleft2 is not None) :
        loc=order
        if p.index==d.index-2: loc+=4
        else: loc+=5
        features['p(p)p(d-2)p(d)o(d,p)='+p.pos+dleft2.pos+d.pos+"_"+str(loc)]=1.0
    if (dright2 is not None) :
        loc=order
        if p.index==d.index+2: loc+=4
        else: loc+=5
        features['p(p)p(d+2)p(d)o(d,p)='+p.pos+dright2.pos+d.pos+"_"+str(loc)]=1.0
    if (pright2 is not None) :
        loc=order
        if p.index+2==d.index: loc+=4
        else: loc+=5
        features['p(p)p(p+2)p(d)o(d,p)='+p.pos+pright2.pos+d.pos+"_"+str(loc)]=1.0
    if (pright1 is not None) :
        loc=order
        if p.index+1==d.index: loc+=4
        elif p.index==d.index-1: loc+=5
        else: loc+=6
        features['p(p)p(p+1)p(p)o(d,p)='+p.pos+pright1.pos+p.pos+"_"+str(loc)]=1.0
    if (pleft1 is not None) :
        loc=order
        if p.index-1==d.index: loc+=4
        elif p.index==d.index+1: loc+=5
        else: loc+=6
        features['p(p)p(p-1)p(p)o(d,p)='+p.pos+pleft1.pos+p.pos+"_"+str(loc)]=1.0
    if (dright1 is not None) :
        loc=order
        if p.index-1==d.index: loc+=4
        elif p.index==d.index+1: loc+=5
        else: loc+=6
        features['p(p)p(d+1)p(d)o(d,p)='+p.pos+dright1.pos+d.pos+"_"+str(loc)]=1.0
    if (dleft1 is not None) :
        loc=order
        if p.index+1==d.index: loc+=4
        elif p.index==d.index-1: loc+=5
        else: loc+=6
        features['p(p)p(d-1)p(d)o(d,p)='+p.pos+dleft1.pos+d.pos+"_"+str(loc)]=1.0
    if (dleft2 is not None) :
        loc=order
        if p.index==d.index-1: loc+=4
        elif p.index==d.index-2: loc+=5
        else: loc+=6
        features['p(p)p(d-2)p(p)o(d,p)='+p.pos+dleft2.pos+p.pos+"_"+str(loc)]=1.0
    if (dright2 is not None) :
        loc=order
        if p.index==d.index+1: loc+=4
        elif p.index==d.index+2: loc+=5
        else: loc+=6
        features['p(p)p(d+2)p(p)o(d,p)='+p.pos+dright2.pos+p.pos+"_"+str(loc)]=1.0
    if (pleft2 is not None) :
        loc=order
        if p.index-1==d.index: loc+=4
        elif p.index-2==d.index: loc+=5
        else: loc+=6
        features['p(p)p(p-2)p(d)o(d,p)='+p.pos+pleft2.pos+d.pos+"_"+str(loc)]=1.0
    if (pright2 is not None) :
        loc=order
        if p.index+1==d.index: loc+=4
        elif p.index+2==d.index: loc+=5
        else: loc+=6
        features['p(p)p(p+2)p(d)o(d,p)='+p.pos+pright2.pos+d.pos+"_"+str(loc)]=1.0
    features['w(p)w(d)p(d)o(d,p)='+p.text+d.text+d.pos+"_"+str(order)]=1.0
    features['w(p)w(d)p(p)o(d,p)='+p.text+d.text+p.pos+"_"+str(order)]=1.0
    features['w(d)w(p)p(d)o(d,p)='+d.text+p.text+d.pos+"_"+str(order)]=1.0
    features['l(p)p(d)o(d,p)='+p.lemma+d.pos+"_"+str(order)]=1.0
    features['l(p)o(d,p)='+p.lemma+"_"+str(order)]=1.0
    features['l(d)p(p)o(d,p)='+d.lemma+p.pos+"_"+str(order)]=1.0
    features['l(d)o(d,p)='+d.lemma+"_"+str(order)]=1.0
    features['l(p)l(d)o(d,p)='+p.lemma+d.lemma+"_"+str(order)]=1.0
    features['l(d)p(p)p(d)l(p)o(d,p)='+d.lemma+p.pos+d.pos+p.lemma+"_"+str(order)]=1.0
    features['l(p)p(p)p(d)o(d,p)='+p.lemma+p.pos+d.pos+"_"+str(order)]=1.0
    features['l(p)p(p)p(d)o(d,p)='+p.lemma+p.pos+d.pos+"_"+str(order)]=1.0
    features['l(p)l(d)p(d)o(d,p)='+p.lemma+d.lemma+d.pos+"_"+str(order)]=1.0
    features['l(p)l(d)p(p)o(d,p)='+p.lemma+d.lemma+p.pos+"_"+str(order)]=1.0
    return features


def create_second_order(p,d,z,role,order,state):
    features={}
    zright1 = get_following(z,'+1',state)
    zleft1 = get_following(z,'-1',state)
    dright1 = get_following(d,'+1',state)
    dleft1 = get_following(d,'-1',state)
    pright1 = get_following(p,'+1',state)
    pleft1 = get_following(p,'-1',state)
    features['p(p)p(d)p(z)o(d,p,z)_'+role+'='+p.pos+d.pos+z.pos+"_"+str(order)]=1.0
    features['p(p)p(z)o(d,p,z)_'+role+'='+p.pos+z.pos+"_"+str(order)]=1.0
    features['p(d)p(z)o(d,p,z)_'+role+'='+d.pos+z.pos+"_"+str(order)]=1.0
    features['w(p)w(z)o(d,p,z)_'+role+'='+p.text+z.text+"_"+str(order)]=1.0
    features['w(d)w(z)o(d,p,z)_'+role+'='+d.text+z.text+"_"+str(order)]=1.0
    features['w(z)p(p)o(d,p,z)_'+role+'='+z.text+p.pos+"_"+str(order)]=1.0
    features['w(z)p(d)o(d,p,z)_'+role+'='+z.text+d.pos+"_"+str(order)]=1.0
    features['w(p)p(z)o(d,p,z)_'+role+'='+p.text+z.pos+"_"+str(order)]=1.0
    features['w(d)p(z)o(d,p,z)_'+role+'='+d.text+z.pos+"_"+str(order)]=1.0
    features['l(p)l(z)o(d,p,z)_'+role+'='+p.lemma+z.lemma+"_"+str(order)]=1.0
    features['l(d)l(z)o(d,p,z)_'+role+'='+d.lemma+z.lemma+"_"+str(order)]=1.0
    features['l(z)p(p)o(d,p,z)_'+role+'='+z.lemma+p.pos+"_"+str(order)]=1.0
    features['l(z)p(d)o(d,p,z)_'+role+'='+z.lemma+d.pos+"_"+str(order)]=1.0
    features['l(p)p(z)o(d,p,z)_'+role+'='+p.lemma+z.pos+"_"+str(order)]=1.0
    features['l(d)p(z)o(d,p,z)_'+role+'='+d.lemma+z.pos+"_"+str(order)]=1.0
    if (zright1 is not None) :
        features['p(z)p(z+1)p(d)o(d,p,z)_'+role+'='+z.pos+zright1.pos+d.pos+"_"+str(order)]=1.0
    if (zleft1 is not None) :
        features['p(z)p(z-1)p(d)o(d,p,z)_'+role+'='+z.pos+zleft1.pos+d.pos+"_"+str(order)]=1.0
    if (dright1 is not None) :
        features['p(z)p(d)p(d+1)o(d,p,z)_'+role+'='+z.pos+d.pos+dright1.pos+"_"+str(order)]=1.0
    if (dleft1 is not None) :
        features['p(z)p(d)p(d-1)o(d,p,z)_'+role+'='+z.pos+d.pos+dleft1.pos+"_"+str(order)]=1.0
    if (dleft1 is not None) and (zright1 is not None) :
        features['p(z)p(z+1)p(d-1)p(d)o(d,p,z)_'+role+'='+z.pos+zright1.pos+dleft1.pos+d.pos+"_"+str(order)]=1.0
    if (dleft1 is not None) and (zleft1 is not None) :
        features['p(z-1)p(z)p(d-1)p(d)o(d,p,z)_'+role+'='+zleft1.pos+z.pos+dleft1.pos+d.pos+"_"+str(order)]=1.0
    if (zright1 is not None) and (dright1 is not None) :
        features['p(z)p(z+1)p(d)p(d+1)o(d,p,z)_'+role+'='+z.pos+zright1.pos+d.pos+dright1.pos+"_"+str(order)]=1.0
    if (zleft1 is not None) and (dright1 is not None) :
        features['p(z-1)p(z)p(d)p(d+1)o(d,p,z)_'+role+'='+zleft1.pos+z.pos+d.pos+dright1.pos+"_"+str(order)]=1.0
    if (zright1 is not None) :
        features['p(z)p(z+1)p(p)o(d,p,z)_'+role+'='+z.pos+zright1.pos+p.pos+"_"+str(order)]=1.0
    if (zleft1 is not None) :
        features['p(z)p(z-1)p(p)o(d,p,z)_'+role+'='+z.pos+zleft1.pos+p.pos+"_"+str(order)]=1.0
    if (pright1 is not None) :
        features['p(z)p(p)p(p+1)o(d,p,z)_'+role+'='+z.pos+p.pos+pright1.pos+"_"+str(order)]=1.0
    if (pleft1 is not None) :
        features['p(z)p(p)p(p-1)o(d,p,z)_'+role+'='+z.pos+p.pos+pleft1.pos+"_"+str(order)]=1.0
    if (zright1 is not None) and (pleft1 is not None) :
        features['p(z)p(z+1)p(p-1)p(p)o(d,p,z)_'+role+'='+z.pos+zright1.pos+pleft1.pos+p.pos+"_"+str(order)]=1.0
    if (zleft1 is not None) and (pleft1 is not None) :
        features['p(z-1)p(z)p(p-1)p(p)o(d,p,z)_'+role+'='+zleft1.pos+z.pos+pleft1.pos+p.pos+"_"+str(order)]=1.0
    if (pright1 is not None) and (zright1 is not None) :
        features['p(z)p(z+1)p(p)p(p+1)o(d,p,z)_'+role+'='+z.pos+zright1.pos+p.pos+pright1.pos+"_"+str(order)]=1.0
    if (pright1 is not None) and (zleft1 is not None) :
        features['p(z-1)p(z)p(p)p(p+1)o(d,p,z)_'+role+'='+zleft1.pos+z.pos+p.pos+pright1.pos+"_"+str(order)]=1.0
    return features


def create_third_order(p,d,y,z,role1,role2,order,state):
    features={}
    yleft1 = get_following(y,'-1',state)
    zleft1 = get_following(z,'-1',state)
    yright1 = get_following(y,'+1',state)
    zright1 = get_following(z,'+1',state)
    features['p(p)p(d)p(z)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+p.pos+d.pos+z.pos+y.pos+"_"+str(order)]=1.0
    features['w(p)p(d)p(z)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+p.text+d.pos+z.pos+y.pos+"_"+str(order)]=1.0
    features['w(d)p(p)p(z)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+d.text+p.pos+z.pos+y.pos+"_"+str(order)]=1.0
    features['w(z)p(d)p(p)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+z.text+d.pos+p.pos+y.pos+"_"+str(order)]=1.0
    features['w(y)p(d)p(z)p(p)o(d,p,y,z)_'+role1+'_'+role2+'='+y.text+d.pos+z.pos+p.pos+"_"+str(order)]=1.0
    features['l(z)p(d)p(p)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+z.lemma+d.pos+p.pos+y.pos+"_"+str(order)]=1.0
    features['l(y)p(d)p(z)p(p)o(d,p,y,z)_'+role1+'_'+role2+'='+y.lemma+d.pos+z.pos+p.pos+"_"+str(order)]=1.0
    features['p(p)p(z)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+p.pos+z.pos+y.pos+"_"+str(order)]=1.0
    features['p(d)p(z)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+d.pos+z.pos+y.pos+"_"+str(order)]=1.0
    features['p(z)p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+z.pos+y.pos+"_"+str(order)]=1.0
    features['p(z)o(d,p,y,z)_'+role1+'_'+role2+'='+z.pos+"_"+str(order)]=1.0
    features['p(y)o(d,p,y,z)_'+role1+'_'+role2+'='+y.pos+"_"+str(order)]=1.0
    if (yleft1 is not None) :
        features['p(p)p(d)p(z)p(y)p(y-1)o(d,p,y,z)_'+role1+'_'+role2+'='+p.pos+d.pos+z.pos+y.pos+yleft1.pos+"_"+str(order)]=1.0
    if (zleft1 is not None) :
        features['p(p)p(d)p(z)p(y)p(z-1)o(d,p,y,z)_'+role1+'_'+role2+'='+p.pos+d.pos+z.pos+y.pos+zleft1.pos+"_"+str(order)]=1.0
    if (yright1 is not None) :
        features['p(p)p(d)p(z)p(y)p(y+1)o(d,p,y,z)_'+role1+'_'+role2+'='+p.pos+d.pos+z.pos+y.pos+yright1.pos+"_"+str(order)]=1.0
    if (zright1 is not None) :
        features['p(p)p(d)p(z)p(y)p(z+1)o(d,p,y,z)_'+role1+'_'+role2+'='+p.pos+d.pos+z.pos+y.pos+zright1.pos+"_"+str(order)]=1.0
    return features
