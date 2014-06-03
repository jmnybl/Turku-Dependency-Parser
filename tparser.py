# -*- coding: utf-8 -*-

import sys
from tree import Token,Tree,Dep, read_conll, fill_conll, write_conll
import codecs
import traceback
from collections import defaultdict
from features import Features
from perceptron import GPerceptron, PerceptronSharedState
import copy

SHIFT=0
RIGHT=1
LEFT=2
SWAP=3

DEPTYPES=u"acomp adpos advcl advmod amod appos aux auxpass ccomp compar comparator complm conj cop csubj csubj-cop dep det dobj gobj gsubj iccomp infmod intj mark name neg nommod nsubj num parataxis partmod poss prt punct rcmod voc xcomp xsubj xsubj-cop nsubj-cop nommod-own csubjpass nn cc number quantmod rel preconj ROOT".split() # TODO: collect these from data


class Transition(object):

    def __init__(self,move,dType=None):
        self.move=move
        self.dType=dType

    def __eq__(self,other):
        return self.move==other.move and self.dType==other.dType

    def __str__(self):
        return str(self.move)+":"+str(self.dType)

    def __repr__(self):
        return str(self.move)+":"+str(self.dType)
   

class State(object):

    def __init__(self,tokens,sent=None):
        self.tree=Tree(tokens,conll=sent)
        self.stack=[]
        self.queue=[Token(-1,u"ROOT",lemma=u"ROOT",pos=u"ROOT",feat=u"ROOT")]
        self.queue+=self.tree.tokens[:]
        self.score=0.0
        self.transitions=[]
        self.features=defaultdict(lambda:0.0)


    def update(self,trans):
        if trans.move==SHIFT: # SHIFT
            self.shift(trans)
        elif trans.move==RIGHT: # RIGHT ARC
            self.add_arc(self.stack[-2],self.stack.pop(-1),trans) 
        elif trans.move==LEFT: # LEFT ARC
            self.add_arc(self.stack[-1],self.stack.pop(-2),trans)
        elif trans.move==SWAP: # SWAP
            self.swap(trans)
        else:
            raise ValueError("Incorrect transition")
        self.transitions.append(trans)
        if len(self.queue)==0 and len(self.stack)==1:
            assert self.stack[-1].index==-1,("ROOT is not the last token in the stack.", self.stack)
            self.tree.ready=True



    def add_arc(self,gov,dep,trans):
        """ Gov and dep are Token class instances. """
        dependency=Dep(gov,dep,trans.dType)
        self.tree.add_dep(dependency)


    def shift(self,trans):
        self.stack.append(self.queue.pop(0))


    def swap(self,trans):
        self.queue.insert(0,self.stack.pop(-2))

    def valid_transitions(self):
        moves=set()
        if len(self.queue)>0: # SHIFT
            moves.add(SHIFT)
        if len(self.stack)>1: # ARCS
            if self.stack[-2].index!=-1: # if s2 is not root
                moves.add(LEFT)
            if  self.stack[-2].index!=-1 or len(self.queue)==0: # Only allow RIGHT from ROOT when queue is empty
                moves.add(RIGHT)
        if len(self.stack)>1 and self.stack[-1].index>self.stack[-2].index and self.stack[-2].index!=-1: # SWAP
            if len(self.queue)==0 and len(self.stack)==2: return moves # no need for swap, we can use simple LEFT or RIGHT 
            moves.add(SWAP)
        return moves

    def __str__(self):
        return (u"Tree ready? "+unicode(self.tree.ready)+u"\nStack: ["+u" ".join(token.text for token in self.stack)+u"]\nQueue: ["+u" ".join(token.text for token in self.queue)+u"]\nScore:"+unicode(self.score)+u"\n"+u"\n".join(u"("+dep.gov.text+u" "+dep.dep.text+u" "+dep.dType+u")" for dep in self.tree.deps)).encode(u"utf-8")

    def __repr__(self):
        return u",".join(str(t.move)+u":"+str(t.dType) for t in self.transitions)


class Parser(object):


    def __init__(self,fName=None,gp=None,test_time=False):
        self.test_time=test_time
        self.features=Features()
        if gp:
            self.perceptron=gp
            return
        elif fName is not None:
            self.perceptron_state=PerceptronSharedState.load(fName,retrainable=True)
        else:
            self.perceptron_state=PerceptronSharedState(5000000)
        self.perceptron=GPerceptron.from_shared_state(self.perceptron_state)


    def train(self,inp,progress=0.0,quiet=False):
        """If inp is string, it will be interpreted as a file, otherwise as open file reading unicode"""
        total=0
        failed=0
        non=0
        for sent in read_conll(inp):
            total+=1
            tokens=u" ".join(t[1] for t in sent)
            gs_tree=Tree(tokens,conll=sent,syn=True)
            #print u" ".join(t.dtype for t in gs_tree.tokens if t.dtype is not None)
            non_projs=gs_tree.is_nonprojective()
            if len(non_projs)>0:
                gs_tree.define_projective_order(non_projs)
                non+=1
            try:
                gs_transitions=self.extract_transitions(gs_tree,tokens)
                self.train_one_sent(gs_transitions,sent,progress) # sent is a conll sentence
            except ValueError:
                #traceback.print_exc()
                # TODO: more than one non-projective dependency
                failed+=1      
        if not quiet:
            print u"Failed to parse:",failed
            print u"Total number of trees:",total
            print u"Non-projectives:",non
            print u"Progress:",progress


    def extract_transitions(self,gs_tree,sent):
        state=State(sent) # note that I don't use conll, so no lemma or pos
        while not state.tree.ready:
            if len(state.queue)==0 and len(state.stack)==2: # only final ROOT arc needed (it's not part of a tree)
                move,=state.valid_transitions() # this is used to decide whether we need LEFT or RIGHT
                assert (move==RIGHT or move==LEFT)
                trans=Transition(move,u"ROOT")
                self.apply_trans(state,trans,feats=False)
                continue
            if len(state.stack)>1:
                move,dType=self.extract_dep(state,gs_tree)
                if move is not None:
                    trans=Transition(move,dType)
                    if trans.move not in state.valid_transitions():
                        raise ValueError("Invalid transition:",trans.move)
                    self.apply_trans(state,trans,feats=False)
                    continue
            # cannot draw arc
            if (len(state.stack)>1) and (gs_tree.projective_order is not None) and (state.stack[-2].index<state.stack[-1].index) and (gs_tree.is_proj(state.stack[-2],state.stack[-1])): # SWAP
                    trans=Transition(SWAP,None)
            else: # SHIFT
                trans=Transition(SHIFT,None)
            if trans.move not in state.valid_transitions():
                raise ValueError("Invalid transition:",trans.move)
            self.apply_trans(state,trans,feats=False)
        return state.transitions
            
    def extract_dep(self,state,gs_tree):
        first,sec=state.stack[-1],state.stack[-2]
        t=gs_tree.has_dep(first,sec)
        if (t is not None) and self.subtree_ready(state,sec,gs_tree):
            return LEFT,t
        t=gs_tree.has_dep(sec,first)
        if (t is not None) and self.subtree_ready(state,first,gs_tree):
            return RIGHT,t
        return None,None      

    def subtree_ready(self,state,tok,gs_tree):
        if len(gs_tree.childs[tok])==0 and len(state.tree.childs[tok])==0: return True
        elif gs_tree.childs[tok]!=state.tree.childs[tok]: return False
        else:
            for child in gs_tree.childs[tok]: return self.subtree_ready(state,child,gs_tree)

    def train_one_sent(self,gs_transitions,sent,progress):
        """ Sent is a list of conll lines."""
        tokens=u" ".join(t[1] for t in sent) # TODO: get rid of this line, this is stupid
        states=[State(tokens,sent=sent)] # create an 'empty' state, use sent (because lemma+pos+feat), but do not fill syntax      
        gs_state=State(tokens,sent=sent) # this not optimal, and we need to rethink this when we implement the beam search
        best=states[0] # hmm, we need 'example case' to check whether we are ready or not
        while not best.tree.ready:
            states=self.give_next_trans(states)# get and apply predicted transition
            best=states[0]
            self.apply_trans(gs_state,gs_transitions[len(best.transitions)-1]) # apply gs transition
            # now we have to check whether gs is still in the beam
            found=False
            for state in states:
                if state.transitions==gs_transitions[:len(state.transitions)]: # check if transition sequence is correct
                    found=True
                    break
            if not found: # correct not in the beam :(
                print len(best.transitions)
#                print states
#                print gs_state.transitions
#                print
                self.perceptron.update(best.features,gs_state.features,best.score,gs_state.score,progress) # update the perceptron
                break
                

#    def parse_sent(self,sent):
#        state=State(sent)
#        #print >> sys.stdout,"Sent:", sent
#        while not state.tree.ready:
#            trans=self.give_next_trans_test(state)
#            if trans.move not in state.valid_transitions():
#                raise ValueError("Invalid transition:",trans.move)
#            self.apply_trans(state,trans)
#        #print state

#    def give_next_trans_test(self,state):
#        global gs_transitions
#        try:
#            #raise ValueError
#            move=gs_transitions.pop(0)
#            trans=Transition(move,"dep")
#            return trans
#        except ValueError:
#            pass
#        try:
#            print state
#            s = raw_input('transition: ')
#            move=int(s)
#        except EOFError:
#            move=0
#        trans=Transition(move,"dep")
#        return trans

    def give_next_trans(self,states):
        """ Predict next transition. """
        if len(states)>40:
            raise ValueError("Beam too big!") # ...for dev time only, to make sure we update the beam correctly
        scores=[]
        for state in states:
            for move in state.valid_transitions():
                if move==RIGHT or move==LEFT:
                    for dType in DEPTYPES:
                        trans=Transition(move,dType)
                        new_state,feats=self.pre_apply(state,trans)
                        scores.append((new_state,feats))
                else:
                    trans=Transition(move,None)
                    new_state,feats=self.pre_apply(state,trans)
                    scores.append((new_state,feats))
        # now we have a master list of states, sort by scores and pick top 40
        new_states=sorted(scores, key=lambda x: x[0].score, reverse=True)[:40] # now we have top 40, yet need to merge features
        beam=[]
        for state,feats in new_states:
            for feat in feats:
                state.features[feat]+=feats[feat] # merge old and new features (needed for perceptron update)
            beam.append(state)
        return beam


    def pre_apply(self,state,trans):
        temp_state=copy.deepcopy(state)
        temp_state.update(trans)
        features=create_all_features(temp_state) # create new features
        temp_state.score+=self.perceptron.score(features) # update score
        return temp_state,features


    def apply_trans(self,state,trans,feats=True):
        """ Use this to apply gs transition. """
        state.update(trans) # update stack and queue
        if not feats: return # we are just extracting transitions from gold tree, no need for features
        features=self.features.create_features(state) # create new features
#        print trans, features
        state.score+=self.perceptron.score(features,self.test_time) # update score # TODO define test_time properly
        for feat in features:
            state.features[feat]+=features[feat] # merge old and new features (needed for perceptron update)

    def parse(self,inp,outp):
        """outp should be a file open for writing unicode"""
        for sent in read_conll(inp):
            tokens=u" ".join(t[1] for t in sent) # TODO: get rid of this line, this is stupid
            state=State(tokens,sent=sent)
            while not state.tree.ready:
                trans=self.give_next_trans(state)
                self.apply_trans(state,trans)
            fill_conll(sent,state)
            write_conll(outp,sent)

            
    


if __name__==u"__main__":

    parser=Parser()
#    parser=Parser(u"full_model",test_time=True)
    
    for i in xrange(0,10):

        print >> sys.stderr, "iter",i+1
        parser.train(u"tdt.conll")
        parser.perceptron_state.save(u"models/perceptron_model_"+str(i+1),retrainable=True)

    outf=codecs.open(u"parserout_test.conll",u"wt",u"utf-8")
    parser.parse(u"test.conll09",outf)
    outf.close()

