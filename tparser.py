# -*- coding: utf-8 -*-

import sys
from tree import Token,Tree,Dep
import codecs
import traceback
import Features
from perceptron import GPerceptron


SHIFT=0
RIGHT=1
LEFT=2
SWAP=3

DEPTYPES=u"acomp adpos advcl advmod amod appos aux auxpass ccomp compar comparator complm conj cop csubj csubj-cop dep det dobj gobj gsubj iccomp infmod intj mark name neg nommod nsubj num parataxis partmod poss prt punct rcmod voc xcomp xsubj xsubj-cop nsubj-cop nommod-own csubjpass nn cc number quantmod rel preconj".split() # TODO: collect these from data


class Transition(object):

    def __init__(self,move,score,dType=None):
        self.move=move
        self.score=score
        self.dType=dType
   

class State(object):

    def __init__(self,sent):
        self.tree=Tree(sent)
        self.stack=[]
        self.queue=self.tree.tokens
        self.score=0.0
        self.transitions=[]


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
        self.transitions.append(trans.move)
        if len(self.queue)==0 and len(self.stack)==1:
            self.tree.ready=True



    def add_arc(self,gov,dep,trans):
        """ Gov and dep are Token class instances. """
        dependency=Dep(gov,dep,trans.dType)
        self.tree.add_dep(dependency)
        self.score+=trans.score


    def shift(self,trans):
        self.stack.append(self.queue.pop(0))
        self.score+=trans.score


    def swap(self,trans):
        self.queue.insert(0,self.stack.pop(-2))
        self.score+=trans.score

    def valid_transitions(self):
        moves=set()
        if len(self.queue)>0: # SHIFT
            moves.add(SHIFT)
        if len(self.stack)>1: # ARCS
            moves.add(RIGHT)
            moves.add(LEFT)
        if len(self.stack)>1 and self.stack[-1].index>self.stack[-2].index: # SWAP
            moves.add(SWAP)
        return moves

    def __str__(self):
        return (u"Tree ready? "+unicode(self.tree.ready)+u"\nStack: ["+u" ".join(token.text for token in self.stack)+u"]\nQueue: ["+u" ".join(token.text for token in self.queue)+u"]\nScore:"+unicode(self.score)+u"\n"+u"\n".join(u"("+dep.gov.text+u" "+dep.dep.text+u" "+dep.dType+u")" for dep in self.tree.deps)).encode(u"utf-8")


class Parser(object):


    def __init__(self):
        self.features=Features()
        self.perceptron=GPerceptron(100)

    def read_conll(self,fName):
        """ Read conll format file and yield one sentence at a time. """
        f=codecs.open(fName,u"rt",u"utf-8")
        sent=[]
        for line in f:
            line=line.strip()
            if not line:
                yield sent # list of conll lines
                sent=[]
            else:
                sent.append(line.split(u"\t"))

    gs_transitions=[]
    def train(self,fName):
        global gs_transitions
        total=0
        failed=0
        non=0
        for sent in self.read_conll(fName):
            total+=1
            tokens=u" ".join(t[1] for t in sent)
            #print tokens
            gs_tree=Tree(tokens,conll=sent)
            non_projs=gs_tree.is_nonprojective()
            if len(non_projs)>0:
                gs_tree.define_projective_order(non_projs)
                print "Orig:",gs_tree.tokens
                print "Proj:",gs_tree.projective_order
                non+=1
            try:
                gs_transitions=self.extract_transitions(gs_tree,tokens)
                self.parse_sent(tokens)
            except ValueError:
                traceback.print_exc()
                # TODO: more than one non-projective dependency
                failed+=1
        print u"Failed to parse:",failed
        print u"Total number of trees:",total
        print u"Non-projectives:",non


    def extract_transitions(self,gs_tree,sent):
        transitions=[]
        state=State(sent)
        while not state.tree.ready:
            #print state
            if len(state.stack)>1:
                move,dType=self.extract_dep(state,gs_tree)
                if move is not None:
                    transitions.append(move)
                    trans=Transition(move,1.0,"dep")
                    if trans.move not in state.valid_transitions():
                        raise ValueError("Invalid transition:",trans.move)
                    self.apply_trans(state,trans)
                    continue
            # cannot draw arc
            if (len(state.stack)>1) and (gs_tree.projective_order is not None) and (gs_tree.tokens.index(state.stack[-2])<gs_tree.tokens.index(state.stack[-1])) and (gs_tree.is_proj(state.stack[-2],state.stack[-1])): # SWAP
                    transitions.append(SWAP)
                    trans=Transition(SWAP,1.0,"dep")
            else: # SHIFT
                transitions.append(SHIFT)
                trans=Transition(SHIFT,1.0,"dep")
            if trans.move not in state.valid_transitions():
                raise ValueError("Invalid transition:",trans.move)
            self.apply_trans(state,trans)
        #print "GS:",gs_tree.deps
        #print "transitions:",transitions
        return transitions
            
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

    def parse_sent(self,sent):
        state=State(sent)
        #print >> sys.stdout,"Sent:", sent
        while not state.tree.ready:
            trans=self.give_next_trans_test(state)
            if trans.move not in state.valid_transitions():
                raise ValueError("Invalid transition:",trans.move)
            self.apply_trans(state,trans)
        #print state

    def give_next_trans_test(self,state):
        global gs_transitions
        try:
            #raise ValueError
            move=gs_transitions.pop(0)
            trans=Transition(move,1.0,"dep")
            return trans
        except ValueError:
            pass
        try:
            print state
            s = raw_input('transition: ')
            move=int(s)
        except EOFError:
            move=0
        trans=Transition(move,1.0,"dep")
        return trans

    def give_next_trans(self,state):
        scores=dict()
        for move in state.valid_transitions():
            if move==RIGHT or move==LEFT:
                for dType in DEPTYPES:
                    trans=Transition(move,1.0,dType)
            else:
                trans=Transition(move,1.0)
            score=self.pre_apply(state,trans)
            scores[(trans.move,trans.dType)]=score

        best_trans=max(scores, key=scores.get)
        return best_trans,scores[best_trans]


    def pre_apply(self,state,trans):
        temp_state=state.copy()
        self.apply_trans(temp_state,trans)
        features=self.features.create_features(temp_state)
        score=self.perceptron.score(features)
        return score


    def apply_trans(self,state,trans):
        state.update(trans)

    


if __name__==u"__main__":

    parser=Parser()

    parser.train(u"tdt.conll")

