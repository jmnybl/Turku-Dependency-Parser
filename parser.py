# -*- coding: utf-8 -*-

import sys
from tree import Token,Tree,Dep

class Transition():

    def __init__(self,move,score,dType=None):
        self.move=move
        self.score=score
        self.dType=dType
        

class State():

    def __init__(self,sent):
        self.queue=sent.split()
        self.stack=[]
        self.tree=Tree(sent)
        self.score=0.0


    def update(self,trans):
        if trans.move==0: # SHIFT
            self.shift(trans)
        elif trans.move==1: # RIGHT ARC
            self.add_arc(self.stack[-2],self.stack.pop(-1),trans) 
        elif trans.move==2: # LEFT ARC
            self.add_arc(self.stack[-1],self.stack.pop(-2),trans)
        else:
            raise Exception("Incorrect transition")
        if len(self.queue)==0 and len(self.stack)==1:
            self.tree.ready=True



    def add_arc(self,gov,dep,trans):
        self.tree.add_dep(gov,dep,trans.dType)
        self.score+=trans.score


    def shift(self,trans):
        self.stack.append(self.queue.pop(0))
        self.score+=trans.score


    def swap(self):
        pass

    def print_text(self):
        print >> sys.stdout, "Tree ready?",self.tree.ready

        print >> sys.stdout, "Stack:",self.stack
        print >> sys.stdout, "Queue:",self.queue
        print >> sys.stdout, "Score:",self.score
        print >> sys.stdout, ""
        for dep in self.tree.deps:
            print >> sys.stdout, dep


class Parser():


    def __init__(self):
        pass

    def train(self):
        pass


    def extract_transitions(self,gs_tree,sent):
        transitions=[]
        state=State(sent)
        while not state.tree.ready:
            if len(state.stack)>1:
                move,dType=self.extract_dep(state,gs_tree)
                if move is not None:
                    transitions.append(move)
                    trans=Transition(move,1.0,"dep")
                    self.apply_trans(state,trans)
                    continue
            # cannot draw arc, shift
            transitions.append(0)
            trans=Transition(0,1.0,"dep")
            self.apply_trans(state,trans)
        print "GS:",gs_tree.deps
        print "transitions:",transitions
        return transitions
            
    def extract_dep(self,state,gs_tree):
        first,sec=state.stack[-1],state.stack[-2]
        t=gs_tree.has_dep(first,sec)
        if (t is not None) and gs_tree.childs[sec]==state.tree.childs[sec]:
            return 2,t
        t=gs_tree.has_dep(sec,first)
        if (t is not None) and gs_tree.childs[first]==state.tree.childs[first]:
            return 1,t
        return None,None      

    def parse_sent(self,sent):
        state=State(sent)
        print >> sys.stdout,"Sent:", sent
        while not state.tree.ready:
            trans=self.give_next_trans(state)
            if trans.move==0 and len(state.queue)==0:
                print >> sys.stderr, "Invalid transition"
                continue
            if (trans.move==1 or trans.move==2) and len(state.stack)<2:
                print >> sys.stderr, "Invalid transition"
                continue
            self.apply_trans(state,trans)
        state.print_text()

    def give_next_trans(self,state):
        # TODO: ML
        try:
            move=gs_transitions.pop(0)
            trans=Transition(move,1.0,"dep")
            return trans
        except:
            pass
        try:
            state.print_text()
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

    tree=Tree("I really like parsing trees .",[("like","really","dep"),("like","I","dep"),('parsing', 'dependency', 'dep'),('like', 'parsing', 'dep'),('like', '.', 'dep')])
    gs_transitions=parser.extract_transitions(tree,"I really like dependency parsing .")
    parser.parse_sent("I really like dependency parsing .")

    tree=Tree("I really like parsing trees .",[("like","really","dep"),("like","I","dep"),('parsing', 'trees', 'dep'),('like', 'parsing', 'dep'),('like', '.', 'dep')])
    gs_transitions=parser.extract_transitions(tree,"I really like parsing trees .")
    parser.parse_sent("I really like parsing trees .")

