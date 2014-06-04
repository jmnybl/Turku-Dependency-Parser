# -*- coding: utf-8 -*-

import sys
import os.path
from tree import Token,Tree,Dep, read_conll, fill_conll, write_conll
import codecs
import traceback
from collections import defaultdict
from features import Features
from perceptron import GPerceptron, PerceptronSharedState
import copy
from model import Model

feats=Features()

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

    def __init__(self,sent=None,syn=False):
        if sent!=None:
            self.tree=Tree.new_from_conll(sent,syn)
            self.queue=self.tree.tokens[:]
        else:
            self.tree=None
            self.queue=[]
        self.stack=[]
        self.queue=[Token(-1,u"ROOT",lemma=u"ROOT",pos=u"ROOT",feat=u"ROOT")]
        self.queue+=self.tree.tokens[:]
        self.score=0.0
        self.transitions=[]
        self.features=defaultdict(lambda:0.0)
        self.prev_state=None #The state from which this one was created, if any

    @classmethod
    def _copy_and_point(cls,s):
        newS=copy.deepcopy(s)
        newS.features={}
        newS.prev_state=s
        return newS

    @classmethod
    def copy_and_point(cls,s):
        newS=cls.__new__(cls)
        newS.queue=s.queue[:]
        newS.stack=s.stack[:]
        newS.score=s.score
        newS.transitions=s.transitions[:]
        newS.prev_state=s
        #newS.tree=copy.deepcopy(s.tree)
        newS.tree=Tree.new_from_tree(s.tree) ###MUST get rid of token.dtype first
        return newS
        
    def create_feature_dict(self):
        """
        Creates the full feature dictionary by assembling the dictionaries
        along the path of states
        """
        d={}
        self._populate_feature_dict(d)
        return d

    def _populate_feature_dict(self,d):
        """
        Recursively populates `d`
        """
        for f,w in self.features.iteritems():
            d[f]=d.get(f,0.0)+w
        if self.prev_state:
            self.prev_state._populate_feature_dict(d)

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
        if os.path.exists(u"corpus_stats.pkl"):
            self.model=Model.load(u"corpus_stats.pkl")
        else:
            self.model=Model.collect(u"corpus_stats.pkl",u"tdt.conll")
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
            gs_tree=Tree.new_from_conll(conll=sent,syn=True)
            non_projs=gs_tree.is_nonprojective()
            if len(non_projs)>0:
                gs_tree.define_projective_order(non_projs)
                non+=1
            try:
                gs_transitions=self.extract_transitions(gs_tree,sent)
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
        state=State(sent,syn=False)
        while not state.tree.ready:
            if len(state.queue)==0 and len(state.stack)==2: # only final ROOT arc needed (it's not part of a tree)
                move,=state.valid_transitions() # this is used to decide whether we need LEFT or RIGHT
                assert (move==RIGHT or move==LEFT)
                trans=Transition(move,u"ROOT")
                state.update(trans)
                continue
            if len(state.stack)>1:
                move,dType=self.extract_dep(state,gs_tree)
                if move is not None:
                    trans=Transition(move,dType)
                    if trans.move not in state.valid_transitions():
                        raise ValueError("Invalid transition:",trans.move)
                    state.update(trans)
                    continue
            # cannot draw arc
            if (len(state.stack)>1) and (gs_tree.projective_order is not None) and (state.stack[-2].index<state.stack[-1].index) and (gs_tree.is_proj(state.stack[-2],state.stack[-1])): # SWAP
                    trans=Transition(SWAP,None)
            else: # SHIFT
                trans=Transition(SHIFT,None)
            if trans.move not in state.valid_transitions():
                raise ValueError("Invalid transition:",trans.move)
            state.update(trans)
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

    def update_and_score_state(self,state,trans):
        """Applies the transition, sets the local features, updates the score"""
        state.update(trans)
        state.features=feats.create_features(state)
        state.score+=self.perceptron.score(state.features,self.test_time)
        

    def train_one_sent(self,gs_transitions,sent,progress):
        """ Sent is a list of conll lines."""
        beam=[State(sent,syn=False)] # create an 'empty' state, use sent (because lemma+pos+feat), but do not fill syntax      
        gs_state=State(sent,syn=False) # TODO this not optimal, and we need to rethink this when we implement the beam search
        while not (self.beam_ready(beam)):
            beam=self.give_next_beam(beam) #This one already calls update_and_score_state()
            if not gs_state.tree.ready: # update gs if it's not ready
                gs_state=State.copy_and_point(gs_state) #okay, this we could maybe avoid TODO @fginter
                gs_trans=gs_transitions[len(gs_state.transitions)]
                if gs_trans.move not in gs_state.valid_transitions():
                    raise ValueError("Invalid GS Transition")
                self.update_and_score_state(gs_state,gs_trans)
            if not self.gold_in_beam(gs_state,beam): # check if gold state is still in beam
                print len(gs_state.transitions)
                self.perceptron.update(beam[0].create_feature_dict(),gs_state.create_feature_dict(),beam[0].score,gs_state.score,progress) # update the perceptron
                break
        else:
            print "*", len(gs_state.transitions)


    def enum_transitions(self,state):
        """Enumerates transition objects allowable for the state. TODO: Filtering here?"""
        for move in state.valid_transitions():
            if move==RIGHT or move==LEFT:
                if move==RIGHT:
                    gov_pos=state.stack[-2].pos
                    dep_pos=state.stack[-1].pos
                else:
                    gov_pos=state.stack[-1].pos
                    dep_pos=state.stack[-2].pos
                allowed=self.model.deptypes.get((gov_pos,dep_pos),set())
                #for dType in DEPTYPES: #FILTERING GOES HERE
                for dType in allowed:
                    yield Transition(move,dType)
                yield Transition(move,u"ROOT") #TODO: what should be done with root?
            else:
                yield Transition(move,None)
                

    def give_next_beam(self,beam):
        """ Predict and create next beam """
        if len(beam)>40:
            raise ValueError("Beam too big!") # ...for dev time only, to make sure we update the beam correctly
        states=[]
        for state in beam:
            if state.tree.ready: # this one is ready, just move it
                states.append(state)
                continue
            for trans in self.enum_transitions(state):
                newS=State.copy_and_point(state)
                self.update_and_score_state(newS,trans)
                states.append(newS)
        new_beam=sorted(states, key=lambda s: s.score, reverse=True)[:40] # now we have top 40
        return new_beam


    def beam_ready(self,beam):
        for state in beam:
            if not state.tree.ready: return False
        return True

    def gold_in_beam(self,gs,beam):
        for state in beam:
            if state.transitions==gs.transitions: return True
        return False


    def parse(self,inp,outp):
        """outp should be a file open for writing unicode"""
        for sent in read_conll(inp):
            beam=[State(sent,syn=False)]
            while not self.beam_ready(beam):
                beam=self.give_next_beam(beam) #This looks wasteful, but it is what the beam will do anyway
            fill_conll(sent,beam[0])
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


