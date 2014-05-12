# -*- coding: utf-8 -*-

import sys
from tree import Token,Tree,Dep
import codecs
import traceback

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


    def update(self,trans):
        if trans.move==0: # SHIFT
            self.shift(trans)
        elif trans.move==1: # RIGHT ARC
            self.add_arc(self.stack[-2],self.stack.pop(-1),trans) 
        elif trans.move==2: # LEFT ARC
            self.add_arc(self.stack[-1],self.stack.pop(-2),trans)
        elif trans.move==3: # SWAP
            self.swap(trans)
        else:
            raise ValueError("Incorrect transition")
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
            moves.add(0)
        if len(self.stack)>1: # ARCS
            moves.add(1)
            moves.add(2)
        if len(self.stack)>1 and self.stack[-1].index>self.stack[-2].index: # SWAP
            moves.add(3)
        return moves

    def __str__(self):
        return (u"Tree ready? "+unicode(self.tree.ready)+u"\nStack: ["+u" ".join(token.text for token in self.stack)+u"]\nQueue: ["+u" ".join(token.text for token in self.queue)+u"]\nScore:"+unicode(self.score)+u"\n"+u"\n".join(u"("+dep.gov.text+u" "+dep.dep.text+u" "+dep.dType+u")" for dep in self.tree.deps)).encode(u"utf-8")


class Parser(object):


    def __init__(self):
        pass

    def read_conll(self,fName):
        sentences=[]
        f=codecs.open(fName,u"rt",u"utf-8")
        lines=[]
        for line in f:
            line=line.strip()
            if not line and len(lines)>0:
                sentences.append(lines)
                lines=[]
            else:
                lines.append(line.split(u"\t"))
        else:
            if len(lines)>0:
                sentences.append(lines)
        return sentences # list of conll lines

    gs_transitions=[]
    def train(self,fName):
        global gs_transitions
        total=0
        failed=0
        non=0
        sentences=self.read_conll(fName)
        for sent in sentences:
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
                    transitions.append(3)
                    trans=Transition(3,1.0,"dep")
            else: # SHIFT
                transitions.append(0)
                trans=Transition(0,1.0,"dep")
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
            return 2,t
        t=gs_tree.has_dep(sec,first)
        if (t is not None) and self.subtree_ready(state,first,gs_tree):
            return 1,t
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
            trans=self.give_next_trans(state)
            if trans.move not in state.valid_transitions():
                raise ValueError("Invalid transition:",trans.move)
            self.apply_trans(state,trans)
        #print state

    def give_next_trans(self,state):
        global gs_transitions
        # TODO: ML
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


    def apply_trans(self,state,trans):
        state.update(trans)

    


if __name__==u"__main__":

    parser=Parser()

    parser.train(u"tdt.conll")

