# -*- coding: utf-8 -*-

from auto_features import create_auto_features, get_from_stack, get_child, get_following, get_from_queue
from auto_features_deptype import create_auto_dep_features

class Features(object):

    def __init__(self):
        pass




    def manual_features(self,state,features):

        S0,S1,S2=get_from_stack(state.stack)
        B0,B1=get_from_queue(state.queue)
        
        ### manually added features ###
        if (S0 is not None) and (S1 is not None): # all of these needs S0 and S1, so check these first
            features[u'SEVAL'+unicode(S0.is_semeval_root)+unicode(S1.is_semeval_root)]=1.0
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

            # morpho queue  
            if (B0 is not None) and (B1 is not None):
                tags0=B0.feat.split(u"|")
                tags1=B1.feat.split(u"|")
                for i in xrange(0,len(tags0)):
                    features['p(S0)p(S1)m(B0)='+S0.pos+S1.pos+tags0[i]]=1.0
                for i in xrange(0,len(tags1)):
                    features['p(S0)p(S1)m(B1)='+S0.pos+S1.pos+tags1[i]]=1.0
                for i in xrange(0,len(tags0)):
                    for j in xrange(0,len(tags1)):
                        features['p(S0)p(S1)m(B0)m(B1)='+S0.pos+S1.pos+tags0[i]+tags1[j]]=1.0
            elif (B0 is not None):
                tags0=B0.feat.split(u"|")
                for i in xrange(0,len(tags0)):
                    features['p(S0)p(S1)m(B0)='+S0.pos+S1.pos+tags0[i]]=1.0


        return features

    def manual_dep_features(self,state,features):
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
        return features


    def create_general_features(self,state):
        feat=create_auto_features(state)
        self.manual_features(state,feat)
        return feat

    def create_deptype_features(self,state):
        feat=create_auto_dep_features(state)
        self.manual_dep_features(state,feat)
        return feat


    def create_features(self, state):
        """ Main function to create all features. """
        feat=self.create_general_features(state)
        feat.update(self.create_deptype_features(state))
        return feat


    
