# -*- coding: utf-8 -*-

import sys
from tree import Token,Tree,Dep, read_conll, fill_conll, write_conll
import codecs
import traceback
from collections import defaultdict
from features import Features
from perceptron import GPerceptron, PerceptronSharedState
import copy

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
    def copy_and_point(cls,s):
        newS=cls.__new__(cls)
        newS.queue=s.queue[:]
        newS.stack=s.stack[:]
        newS.score=s.score
        newS.transitions=s.transitions[:]
        newS.prev_state=s
        newS.tree=Tree.new_from_tree(s.tree)
        return newS

    @classmethod
    def clone_and_apply_dep(cls,s,dep,tr): 
        """
        Makes an exact copy of the state, applies dep, and copies purely only
        what differentiates the new state w.r.t. the dep. Sort of "copy-on-write" of a kind
        """
        newS=copy.copy(s)
        newS.tree=Tree.clone(s.tree) #Copies only deps and dTypes, clones rest
        newS.tree.add_dep_private(dep) #Only changes parts relevant to dType, leaves rest unmodified
        newS.transitions=s.transitions[:]
        newS.transitions.append(tr)
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

    def update_QS(self,trans):
        #Only update the queue and stack, return Dep() if applicable, None otherwise
        if trans.move==SHIFT: # SHIFT
            self.stack.append(self.queue.pop(0))
            d=None
        elif trans.move==RIGHT: # RIGHT ARC
            d=Dep(self.stack[-2],self.stack.pop(-1),trans.dType)
        elif trans.move==LEFT: # LEFT ARC
            d=Dep(self.stack[-1],self.stack.pop(-2),trans.dType)
        elif trans.move==SWAP: # SWAP
            self.queue.insert(0,self.stack.pop(-2))
            d=None
        else:
            raise ValueError("Incorrect transition")
        if len(self.queue)==0 and len(self.stack)==1:
            assert self.stack[-1].index==-1,("ROOT is not the last token in the stack.", self.stack)
            self.tree.ready=True
        return d
        

    def update(self,trans):
        d=self.update_QS(trans)
        if d!=None:
            self.tree.add_dep(d)
        self.transitions.append(trans)


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

    def score_state(self,state):
        state.features=feats.create_features(state)
        state.score+=self.perceptron.score(state.features,self.test_time)

    def update_and_score_state(self,state,trans):
        """Applies the transition, sets the local features, updates the score"""
        state.update(trans)
        self.score_state(state)
        

    def train_one_sent(self,gs_transitions,sent,progress):
        """ Sent is a list of conll lines."""
        state=State(sent,syn=False) # create an 'empty' state, use sent (because lemma+pos+feat), but do not fill syntax      
        gs_state=State(sent,syn=False) # TODO this not optimal, and we need to rethink this when we implement the beam search
        while not state.tree.ready:
            state=self.give_next_state(state) #This one already calls update_and_score_state()
            gs_state=State.copy_and_point(gs_state) #okay, this we could maybe avoid TODO @fginter
            gs_trans=gs_transitions[len(state.transitions)-1]
            self.update_and_score_state(gs_state,gs_trans)
            if state.transitions!=gs_transitions[:len(state.transitions)]: # check if transition sequence is incorrect
                print len(state.transitions)
                self.perceptron.update(state.create_feature_dict(),gs_state.create_feature_dict(),state.score,gs_state.score,progress) # update the perceptron
                break
        else:
            print "*", len(state.transitions)


    def enum_transitions(self,state):
        """Enumerates transition objects allowable for the state. TODO: Filtering here?"""
        for move in state.valid_transitions():
            if move==RIGHT or move==LEFT:
                for dType in DEPTYPES: #FILTERING GOES HERE
                    yield Transition(move,dType)
            else:
                yield Transition(move,None)
                
    def give_next_state(self,state):
        """ Predict next state and create it """
        states=[]
        valid=state.valid_transitions()
        if RIGHT in valid:
            RA_prototype=State.copy_and_point(state) #This one we will then clone
            dep_RA=RA_prototype.update_QS(Transition(RIGHT,None)) #moves the stack/queue, returns Dep() with empty type
            RA_prototype.tree.add_dep_shared(dep_RA)
        if LEFT in valid:
            LA_prototype=State.copy_and_point(state) #This one we will then clone
            dep_LA=LA_prototype.update_QS(Transition(LEFT,None)) #moves the stack/queue, returns Dep() with empty type
            LA_prototype.tree.add_dep_shared(dep_LA)
        #LA_ and RA_ prototypes are now states with LEFT/RIGHT arc applied except for type-dependent parts, these will then be cloned as needed
        for trans in self.enum_transitions(state):
            if trans.move==LEFT:
                d=copy.copy(dep_LA)
                d.dType=trans.dType #Make a new dependency
                newS=State.clone_and_apply_dep(LA_prototype,d,trans)
                self.score_state(newS)
            elif trans.move==RIGHT:
                d=copy.copy(dep_RA)
                d.dType=trans.dType #Make a new dependency
                newS=State.clone_and_apply_dep(RA_prototype,d,trans)
                self.score_state(newS)
            else:
                newS=State.copy_and_point(state)
                self.update_and_score_state(newS,trans)
            states.append(newS)
        best_state=max(states, key=lambda s: s.score)
        return best_state



    def parse(self,inp,outp):
        """outp should be a file open for writing unicode"""
        for sent in read_conll(inp):
            state=State(sent,syn=False)
            while not state.tree.ready:
                state=self.give_next_state(state) #This looks wasteful, but it is what the beam will do anyway
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


