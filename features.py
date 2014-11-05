# -*- coding: utf-8 -*-

from auto_features import create_auto_features, get_from_stack, get_child, get_following, get_from_queue
from auto_features_deptype import create_auto_dep_features
from auto_graph_features_corrected import create_first_order,create_second_order,create_third_order

RIGHT=1
LEFT=2

class Features(object):

    def __init__(self):
        pass




    def manual_features(self,state,features):

        S0,S1,S2=get_from_stack(state.stack)
        B0,B1=get_from_queue(state.queue)
        
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
                v0=get_following(S1,idx_1,state)
                for idx_0 in ['-1','+1']:
                    v1=get_following(S0,idx_0,state)
                    if (v0 is not None) and (v1 is not None):
                        features['p(S'+idx_1+'1)p(S'+idx_0+'0)w(S0)='+v0.pos+v1.pos+S0.text]=1.0
                        features['p(S1)p(S0)p(S'+idx_1+'1)p(S'+idx_0+'0)='+S1.pos+S0.pos+v0.pos+v1.pos]=1.0
            for idx_1 in ['-2','+2']:
                v0=get_following(S1,idx_1,state)
                for idx_0 in ['-2','+2']:
                    v1=get_following(S0,idx_0,state)
                    if (v0 is not None) and (v1 is not None):
                        features['p(S1)p(S0)p(S'+idx_1+'1)p(S'+idx_0+'0)='+S1.pos+S0.pos+v0.pos+v1.pos]=1.0

            # morpho stack
            tags0=S0.feat.split(u"|")
            tags1=S1.feat.split(u"|")
            for i in xrange(0,len(tags0)):
                features['p(S0)p(S1)m(S0)='+S0.pos+S1.pos+tags0[i]]=1.0
            for i in xrange(0,len(tags1)):
                features['p(S0)p(S1)m(S1)='+S0.pos+S1.pos+tags1[i]]=1.0
            for i in xrange(0,len(tags0)):
                for j in xrange(0,len(tags1)):
                    features['p(S0)p(S1)m(S0)m(S1)='+S0.pos+S1.pos+tags0[i]+tags1[j]]=1.0

            # prefixes and suffixes
            features[u"p(S0)p1(S0)p1(S1)="+S0.pos+S0.text[:2]+S1.text[:2]]=1.0
            features[u"p(S0)s1(S0)s1(S1)="+S0.pos+S0.text[-2:]+S1.text[-2:]]=1.0
            features[u"p(S0)p2(S0)s3(S1)="+S0.pos+S0.text[:3]+S1.text[-4:]]=1.0
            features[u"p(S0)s3(S0)p2(S1)="+S0.pos+S0.text[-4:]+S1.text[:3]]=1.0

            # queue  
            if (B0 is not None):
                tags0=B0.feat.split(u"|")
                for i in xrange(0,len(tags0)):
                    features['p(S0)p(S1)m(B0)='+S0.pos+S1.pos+tags0[i]]=1.0
                # prefixes and suffixes
                features[u"p(B0)p2(B0)="+B0.pos+B0.text[:3]]=1.0
                features[u"p(B0)s2(B0)="+B0.pos+B0.text[-3:]]=1.0
                features[u"p(B0)p1(B0)p1(S0)="+B0.pos+B0.text[-2:]+S0.text[:2]]=1.0
                features[u"p(S0)w(B0)s1(S0)="+S0.pos+B0.text+S0.text[-2:]]=1.0
                features[u"p(S0)w(B0)s2(S0)="+S0.pos+B0.text+S0.text[-3:]]=1.0
                # morpho
                if (B1 is not None):
                    tags1=B1.feat.split(u"|")
                    for i in xrange(0,len(tags1)):
                        features['p(S0)p(S1)m(B1)='+S0.pos+S1.pos+tags1[i]]=1.0
                    for i in xrange(0,len(tags0)):
                        for j in xrange(0,len(tags1)):
                            features['p(S0)p(S1)m(B0)m(B1)='+S0.pos+S1.pos+tags0[i]+tags1[j]]=1.0

        return features

    def manual_dep_features(self,state,features,factors):
        """ Add here features involving dependency type. """
        # transition history
        if len(state.stack)>0:
            if len(state.transitions)>3:
                transit=state.transitions[len(state.transitions)-4:][::-1]
            else: 
                transit=state.transitions[::-1]
            for i in xrange(0,len(transit)):
                name='p(S0)h'+'h'.join(str(j) for j in xrange(0,i+1)) # feature name
                value=state.stack[-1].pos+''.join(str(t.move)+str(t.dType) for t in transit[:i+1]) # feature 'value'
                features[name+'='+value]=1.0
        # graph-based features
        if len(state.tree.deps)>0:
            
            g=state.tree.deps[-1].gov
            d=state.tree.deps[-1].dep
            for factor in factors:
                if len(factor)==3: # second order
                    dtype=unicode(state.tree.dtypes.get(factor[0]))
                    features[u"grfp(p)p(d)p(z)d(z)_"+factor[1]+u"="+g.pos+d.pos+factor[0].pos+dtype+u"_"+unicode(factor[2])]=1.0
                    features[u"grfp(p)p(z)d(z)_"+factor[1]+u"="+g.pos+factor[0].pos+dtype+u"_"+unicode(factor[2])]=1.0
                    features[u"grfp(d)d(z)_"+factor[1]+u"="+d.pos+dtype+u"_"+unicode(factor[2])]=1.0
                    features[u"grfp(p)d(z)_"+factor[1]+u"="+g.pos+dtype+u"_"+unicode(factor[2])]=1.0
                    features[u"grfp(z)d(z)_"+factor[1]+u"="+factor[0].pos+dtype+u"_"+unicode(factor[2])]=1.0
                    features[u"grfd(z)_"+factor[1]+u"="+dtype+u"_"+unicode(factor[2])]=1.0
                elif len(factor)==5: # third order
                    dtype1=unicode(state.tree.dtypes.get(factor[0]))
                    dtype2=unicode(state.tree.dtypes.get(factor[2]))
                    features[u"grfp(p)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+g.pos+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfp(d)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+d.pos+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfp(z)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+factor[2].pos+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfp(y)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+factor[0].pos+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfw(p)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+g.text+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfw(d)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+d.text+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfw(z)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+factor[2].text+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                    features[u"grfw(y)d(y)d(z)_"+factor[1]+u"_"+factor[3]+u"="+factor[0].text+dtype1+dtype2+u"_"+unicode(factor[4])]=1.0
                else:
                    assert False # should never happen...


    def factor_location(self,p,d,x=None,z=None):
        """ Map the ordering of tokens to unique integer. """
        loc=0
        if d.index<p.index:
            loc+=1
        if x is None and z is None:
            return loc
        if x.index<d.index:
            loc+=2
        if x.index<p.index:
            loc+=4
        if z is None:
            return loc
        if z.index<x.index:
            loc+=8
        if z.index<p.index:
            loc+=16
        if z.index<d.index:
            loc+=32
        return loc
        

    def new_factors(self,state):
        g=state.tree.deps[-1].gov
        d=state.tree.deps[-1].dep
        factors=[]
        # now collect cmi, cmo, ci, cho, ch1, ch2, cm1, cm2 and tmo
        deps=sorted(state.tree.childs[g]) # cho,ci
        for dep in deps:
            if dep==d: continue
            order=self.factor_location(g,d,dep)
            if order==5 or order==2:
                factors.append([dep,u"ci",order])
            elif order==1 or order==6 or order==7 or order==0:
                factors.append([dep,u"cho",order])
            else:
                assert False # should never happen...
        if len(deps)>2: ## ch1 and ch2
            ch1=deps[0] if deps[0]!=d else deps[1]
            ch2=deps[1] if (deps[1]!=ch1 and deps[1]!=d) else deps[2]
            order=self.factor_location(g,d,ch1,ch2)
            factors.append([ch1,u"ch1",ch2,u"ch2",order])
        deps=sorted(state.tree.childs[d]) # cmi,cmo
        for dep in deps:
            order=self.factor_location(g,d,dep)
            if order==2 or order==5:
                factors.append([dep,u"cmi",order])
            elif order==0 or order==7 or order==1 or order==6:
                factors.append([dep,u"cmo",order])
            else:
                assert False # should never happen...
        if len(deps)>1: # cm1, cm2
            cm1=deps[0]
            cm2=deps[1]
            order=self.factor_location(g,d,cm1,cm2)
            factors.append([cm1,u"cm1",cm2,u"cm2",order])
        ## tmo
        if len(deps)>0:
            rightmost=deps[-1]
            deps_of_rightmost=sorted(state.tree.childs[rightmost])
            if len(deps_of_rightmost)>0:
                tmo=deps_of_rightmost[-1]
                order=self.factor_location(g,d,rightmost,tmo)
                factors.append([rightmost,u"cmo",tmo,u"tmo",order])
        return factors
                


    def create_general_features(self,state):
        feat=create_auto_features(state)
        self.manual_features(state,feat)
        # now graph-based features...
        if state.transitions[-1].move==RIGHT or state.transitions[-1].move==LEFT:
            factors=self.new_factors(state)
            g=state.tree.deps[-1].gov
            d=state.tree.deps[-1].dep
            fact_feats=create_first_order(g,d,self.factor_location(g,d),state)
            for factor in factors:
                if len(factor)==3: # second order
                    fact_feats.update(create_second_order(g,d,factor[0],factor[1],factor[2],state))
                    ## morpho
                    tags0=g.feat.split(u"|")
                    tags1=d.feat.split(u"|")
                    tags2=factor[0].feat.split(u"|")
                    for i in xrange(0,len(tags0)):
                        for j in xrange(0,len(tags2)):
                            fact_feats['grfp(p)p(z)m(p)m(z)='+g.pos+factor[0].pos+tags0[i]+tags2[j]+u"_"+factor[1]]=1.0
                    for i in xrange(0,len(tags1)):
                        for j in xrange(0,len(tags2)):
                            fact_feats['grfp(d)p(z)m(d)m(z)='+d.pos+factor[0].pos+tags1[i]+tags2[j]+u"_"+factor[1]]=1.0

                elif len(factor)==5: # third order
                    fact_feats.update(create_third_order(g,d,factor[0],factor[2],factor[1],factor[3],factor[4],state))
                else:
                    assert False # should never happen...
                
            ## manual first order features
            # for all x between g and d, p(g)p(d)p(x)
            if self.factor_location(g,d)==0:
                tokens=state.tree.tokens[g.index+1:d.index]
            else:
                tokens=state.tree.tokens[d.index+1:g.index]
            for x in tokens:
                fact_feats[u"grfp(g)p(d)p(x)="+g.pos+d.pos+x.pos]=1.0
            # morpho g,d
            tags0=g.feat.split(u"|")
            tags1=d.feat.split(u"|")
            for i in xrange(0,len(tags0)):
                fact_feats['grfp(p)p(d)m(p)='+g.pos+d.pos+tags0[i]+u"_"+unicode(self.factor_location(g,d))]=1.0
            for i in xrange(0,len(tags1)):
                fact_feats['grfp(p)p(d)m(d)='+g.pos+d.pos+tags1[i]+u"_"+unicode(self.factor_location(g,d))]=1.0
            for i in xrange(0,len(tags0)):
                for j in xrange(0,len(tags1)):
                    fact_feats['grfp(p)p(d)m(p)m(d)='+g.pos+d.pos+tags0[i]+tags1[j]+u"_"+unicode(self.factor_location(g,d))]=1.0

            feat.update(fact_feats) ## mix with normal features
        else:
            factors=[]

        return feat, factors

    def create_deptype_features(self,state,factors):
        feat=create_auto_dep_features(state)
        self.manual_dep_features(state,feat,factors)
        return feat


    def create_features(self, state):
        """ Main function to create all features. GS state uses this one. """
        feat,factors=self.create_general_features(state)
        feat.update(self.create_deptype_features(state,factors))
        return feat


    
