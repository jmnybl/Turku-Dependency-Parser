# -*- coding: utf-8 -*-

class Features(object):

    def __init__(self):
        pass

    def get_from_stack(self,stack):
        """ Return needed tokens from stack. """
        if len(stack)>1:
            return stack[-1],stack[-2]
        elif len(stack)>0:
            return stack[-1],None
        else:
            return None,None

    def get_followings(self,token):
        """ The immediately following words of token in input string (not the same than queue!)"""
        # TODO: currently state does not have this information
        return None,None

    def get_leftchilds(self,token,tree):
        """ Return leftmost childs of given token. """
        childs=sorted(tree.childs[token], lambda x:x.index)
        if len(childs)>1:
            return childs[0],childs[1]
        elif len(childs)>0:
            return childs[0],None
        else:
            return None,None


    def create_unigram_features(self, state):
        """
        Unigram features:
        The top two words of the stack (s0, s1)
        The two following words of s0 in input string (s0f0,s0f1)
        The two leftmost children of s0 (s0ld0, s0ld1)
        """
        uni_feat=dict()
        s0,s1=self.get_from_stack(state.stack) # two words of the stack
        uni_feat[s0.text]=1.0 # word form
        uni_feat[s1.text]=1.0
        # TODO: take final POS, lemma

        s0f0,s0f1=self.get_followings(s0)
        # TODO: take final POS

        s0ld0,s0ld1=self.get_leftchilds(s0,state.tree)
        # TODO: take word form

        return uni_feat

    def create_features(self, state)
        features=dict()
        features.update(self.create_unigram_features(state))
        return features


    
