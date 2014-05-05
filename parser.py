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
        self.tree=Tree()
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



class Parser():


    def __init__(self):
        pass

    def train(self):
        pass

    def parse_sent(self,sent):
        state=State(sent)
        print >> sys.stdout, state.queue
        while not state.tree.ready:
            trans=self.give_next_trans(state)
            if trans.move==0 and len(state.queue)==0:
                print >> sys.stderr, "Invalid transition"
                continue
            if (trans.move==1 or trans.move==2) and len(state.stack)<2:
                print >> sys.stderr, "Invalid transition"
                continue
            self.apply_trans(state,trans)
            self.print_state(state)
        self.print_state(state)

    def give_next_trans(self,state):
        # TODO: ML
        try:
            s = raw_input('transition: ')
            move=int(s)
        except EOFError:
            move=0
        trans=Transition(move,1.0,"dep")
        return trans


    def apply_trans(self,state,trans):
        state.update(trans)

    def print_state(self,state):
        print >> sys.stdout, "Tree ready?",state.tree.ready

        print >> sys.stdout, "Stack:",state.stack
        print >> sys.stdout, "Queue:",state.queue
        print >> sys.stdout, "Score:",state.score
        print >> sys.stdout, ""
        for dep in state.tree.deps:
            print >> sys.stdout, dep


if __name__==u"__main__":

    parser=Parser()
    parser.parse_sent("I really like dependency parsing .")

