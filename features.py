# -*- coding: utf-8 -*-

from auto_features import create_auto_features, get_from_stack, get_child, get_following

class Features(object):

    def __init__(self):
        pass


    def get_transitions(self,state):
        """ Return as many as found, max 4 (as a list) """
        transit=[]
        for trans in reversed(state.transitions):
            transit.append(trans)
            if len(transit)>4:
                return transit
        return transit


    def manual_features(self,state):
        features={}
        S0,S1,S2=get_from_stack(state.stack)
        
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
            transit=self.get_transitions(state)
            if transit:
                for i in xrange(0,len(transit)):
                    name='p(S0)h'+'h'.join(str(j) for j in xrange(0,i+1)) # feature name
                    value=S0.pos+''.join(str(t.move)+str(t.dType) for t in transit[:i+1]) # feature 'value'
                    features[name+'='+value]=1.0

        return features



    def create_features(self, state):
        """ Main function to create all features. """
        feat=create_auto_features(state)
        feat.update(self.manual_features(state))
        return feat


    
