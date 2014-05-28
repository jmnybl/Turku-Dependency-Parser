# -*- coding: utf-8 -*-

from auto_features import create_all_features

class Features(object):

    def __init__(self):
        pass

    def get_from_stack(self,stack):
        """ Return needed tokens from the stack. """
        if len(stack)>1:
            return stack[-1],stack[-2]
        elif len(stack)>0:
            return stack[-1],None
        else:
            return None,None

    def get_from_queue(self,queue):
        """ Return needed tokens from the queue. """
        if len(queue)>1:
            return queue[0],queue[1]
        elif len(queue)>0:
            return queue[0],None
        else:
            return None,None

    def get_followings(self,token):
        """ The immediately following words of a token in input string (not the same than queue!)"""
        # TODO: currently state does not have this information
        return None,None

    def get_leftchilds(self,token,tree):
        """ Return two leftmost children of a given token. """
        childs=sorted(tree.childs[token], key=lambda x:x.index)
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
        The two following words of s0 in input string (s0f0, s0f1)
        The two leftmost children of s0 (s0ld0, s0ld1)
        """
        ## TODO: what kind of prefixes should I use?
        uni_feat=dict()

        s0,s1=self.get_from_stack(state.stack) # stack
        l=[s0,s1]
        for i in xrange(0,len(l)):
            token=l[i]
            if token is not None:
                uni_feat[u"stack"+str(i)+"="+token.text]=1.0 # word form
                uni_feat[u"stack"+str(i)+"="+token.pos]=1.0 # pos
                uni_feat[u"stack"+str(i)+"="+token.lemma]=1.0 # lemma
                uni_feat[u"stack"+str(i)+"="+token.feat]=1.0 # morphological features (extra feature for Finnish)

        q0,q1=self.get_from_queue(state.queue) # queue
        l=[q0,q1]
        for i in xrange(0,len(l)):
            token=l[i]
            if token is not None:
                uni_feat[u"queue"+str(i)+"="+token.text]=1.0 # word form
                uni_feat[u"queue"+str(i)+"="+token.pos]=1.0 # pos
                uni_feat[u"queue"+str(i)+"="+token.lemma]=1.0 # lemma
                uni_feat[u"queue"+str(i)+"="+token.feat]=1.0 # morphological features (extra feature for Finnish)

        ## depType
        uni_feat[u"dType="+str(state.transitions[-1].dType)]=1.0

        s0f0,s0f1=self.get_followings(s0) # following
        for token in [s0f0,s0f1]:
            if token is not None:
                uni_feat[u"following="+token.pos]

        s0ld0,s0ld1=self.get_leftchilds(s0,state.tree) # subtree
        for token in [s0ld0,s0ld1]:
            if token is not None:
                uni_feat[u"leftchild="+token.text]=1.0

        


        return uni_feat

    def create_bigram_features(self, state):
        """
        Bigram features:
        The top two words of the stack (s0, s1)
        The two following words of s0 in input string (s0f0, s0f1)
        Previous transition (h0)
        """
        bi_feat=dict()
        s0,s1=self.get_from_stack(state.stack) # stack
        if (s0 is not None) and (s1 is not None):
            bi_feat[u"bigram-stack="+s1.text+s0.pos]=1.0
            bi_feat[u"bigram-stack="+s1.pos+s0.text]=1.0
            bi_feat[u"bigram-stack="+s0.text+s0.pos]=1.0
            bi_feat[u"bigram-stack="+s0.text+s1.pos]=1.0
            bi_feat[u"bigram-stack="+s1.text+s0.text]=1.0
            bi_feat[u"bigram-stack="+s1.lemma+s0.pos]=1.0
            bi_feat[u"bigram-stack="+s1.pos+s0.lemma]=1.0
            bi_feat[u"bigram-stack="+s1.pos+s0.pos]=1.0
            if len(state.transitions)>1:
                bi_feat[u"bigram-stack="+s0.pos+str(state.transitions[-2].move)]=1.0
        

        q0,q1=self.get_from_queue(state.queue) # queue
        if (q0 is not None) and (q1 is not None):
            bi_feat[u"bigram-queue="+q1.text+q0.pos]=1.0
            bi_feat[u"bigram-queue="+q1.pos+q0.text]=1.0
            bi_feat[u"bigram-queue="+q0.text+q0.pos]=1.0
            bi_feat[u"bigram-queue="+q0.text+q1.pos]=1.0
            bi_feat[u"bigram-queue="+q1.text+q0.text]=1.0
            bi_feat[u"bigram-queue="+q1.lemma+q0.pos]=1.0
            bi_feat[u"bigram-queue="+q1.pos+q0.lemma]=1.0
            bi_feat[u"bigram-queue="+q1.pos+q0.pos]=1.0
            if len(state.transitions)>1:
                bi_feat[u"bigram-queue="+q0.pos+str(state.transitions[-2].move)]=1.0
    
        s0f0,s0f1=self.get_followings(s0) # following


        return bi_feat


    def create_features(self, state):
        """ Main function to create all features. """
#        features=dict()
#        features.update(self.create_unigram_features(state))
#        features.update(self.create_bigram_features(state))
#        return features
        feat=create_all_features(state)
        #print feat
        return feat


    
