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
        self._populate_feature_dict(d,prefix=None) #TODO: What exactly we should do with the very last state, it doesn't have any transition prefix...
        return d

    def _populate_feature_dict(self,d,prefix):
        """
        Recursively populates `d`
        """
        if prefix!=None: #Will not extract information from the final state, but that probably makes no difference at all
            for f,w in self.features.iteritems():
                d[prefix+f]=d.get(f,0.0)+w
        if self.prev_state:
            self.prev_state._populate_feature_dict(d,str(self.transitions[-1])) #Use the last transition as the prefix for the state which resulted in this one

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


    def update_and_score_state(self,state,trans):
        """Applies the transition, sets the local features, updates the score"""
        state.update(trans)
        state.features=feats.create_features(state)
        state.score+=self.perceptron.score(state.features,self.test_time)

    def update_and_score_partial(self,state,trans):
        """Applies the transition, sets the local, deptype related features, updates the score calculated from deptype related features."""
        state.update(trans)
        state.features=feats.create_deptype_features(state)
        state.score+=self.perceptron.score(state.features,self.test_time)
        

    def train_one_sent(self,gs_transitions,sent,progress):
        """ Sent is a list of conll lines."""
        try:
            best_state=State(sent,syn=False) # create an 'empty' state, use sent (because lemma+pos+feat), but do not fill syntax      
            gs_state=State(sent,syn=False) # TODO this not optimal, and we need to rethink this when we implement the beam search
            while not best_state.tree.ready:
                new_states=self.give_next_state(best_state) #This one already calls update_and_score_state()
                best_state=new_states[0]
                if len(new_states)>1:
                    state2nd=new_states[1]
                else:
                    state2nd=None
                
                # Okay, maybe we could find the GS state while we are in .give_next_state()
                # but let's keep a general solution and    
                # build it separately
                # This here pretty much mirrors to what happens in .give_next_state()
                #print "GT: ",gs_transitions
                #print "BS: ",best_state.transitions
                #print "GS: ",gs_state.transitions
                
                gs_trans=gs_transitions[len(best_state.transitions)-1]
                s=self.perceptron.score(gs_state.features,False,prefix=str(gs_trans))
                gs_state=State.copy_and_point(gs_state) #okay, this we could maybe avoid TODO @fginter
                gs_state.score+=s
                gs_state.update(gs_trans)
                gs_state.features=feats.create_features(gs_state)
                #
                #print "GS: ",gs_state.transitions
                #print
                # One big problem here is that since we use feature prefixes to differentiate transitions
                # the perceptron update() must be aware of this
                # this is implemented in create_feature_dict()
                # basically the last transition applied in any state, is the prefix to be used for features from
                # the previous state. This is what create_feature_dict() does.

                if best_state.transitions!=gs_transitions[:len(best_state.transitions)]: # check if transition sequence is incorrect
                    prog=float(len(best_state.transitions))/len(gs_transitions)
                    print "%.01f%%     %d/%d  "%(prog*100.0,len(best_state.transitions),len(gs_transitions))
                    sys.stdout.flush()
                    self.perceptron.update(best_state.create_feature_dict(),gs_state.create_feature_dict(),best_state.score,gs_state.score,progress) # update the perceptron
                    break
                elif state2nd is not None and best_state.score-state2nd.score<1.0: #Prediction OK, but no margin
                    #print "+%d"%(len(best_state.transitions)),
#                    print "+", len(state.transitions)
                    #Update and continue training...
                    self.perceptron.update(state2nd.create_feature_dict(),best_state.create_feature_dict(),state2nd.score,best_state.score,progress) # update the perceptron
            else:
                #Check the margin and update if <1
                print "...:)", len(best_state.transitions)
                sys.stdout.flush()
            #Done with the example
            self.perceptron.add_to_average()
        except:
            raise


    def enum_transitions(self,state):
        """Enumerates transition objects allowable for the state. TODO: Filtering here?"""
        for move in state.valid_transitions():
            if move==RIGHT or move==LEFT:
                for dType in DEPTYPES: #FILTERING GOES HERE
                    yield Transition(move,dType)
            else:
                yield Transition(move,None)
                
    def give_next_state(self,state):
        """ Predict next state and creates it. Also returns the next best state, needed for the margin update """
        #We want to
        # 1) go over the allowed transitions and score each state with that operation's prefix
        # 2) apply the next transition

        #Rank the state w.r.t. every possible transition, use str(trans) as the prefix to differentiate features
        scores=[] #Holds (score,transition) tuples
        for trans in self.enum_transitions(state):
            s=self.perceptron.score(state.features,self.test_time,prefix=str(trans))
            scores.append((s,trans))
        #Okay, now we have the possible continuations ranked
        selected_transitions=[] #These will be the selected transitions to use (as a list to make it easy to modify for beam)
                    #right now I'll put there only the best and second best transitions
        selected_transitions.append(max(scores)) #best (score,transition) pair
        scores.remove(selected_transitions[0]) #inefficient, but surely better than sort() at this point
        if scores: #will be empty if only a single transition was allowed
            selected_transitions.append(max(scores)) #2nd best (score,transition) pair

        #So now I know the N (right now two) best transitions to work with, in beam, this would be a lot more of course, max beam-width, though
        selected_states=[] 
        lfeats,lscore=None,None # Holds shared features and score for left transition
        rfeats,rscore=None,None
        for score,transition in selected_transitions:
            #For each of these, we will now create a new state and build its features while we are at it, because now is the time to do it efficiently
            newS=State.copy_and_point(state)
            newS.update(transition)
            newS.score+=score
            newS.features=feats.create_deptype_features(newS) #These are different for every of these states
            if trans.move==LEFT:
                if lfeats is None: # create these features
                    lfeats=feats.create_general_features(newS)
                newS.features.update(lfeats)
            elif trans.move==RIGHT:
                if rfeats is None:
                    rfeats=feats.create_general_features(newS)
                newS.features.update(rfeats)
            else:
                newS.features.update(feats.create_general_features(newS))
            selected_states.append(newS)
        return selected_states #List of selected states, ordered by their score in this move



    def parse(self,inp,outp):
        """outp should be a file open for writing unicode"""
        for sent in read_conll(inp):
            state=State(sent,syn=False)
            while not state.tree.ready:
                new_states=self.give_next_state(state) #This looks wasteful, but it is what the beam will do anyway
                state=new_states[0]
            fill_conll(sent,state)
            write_conll(outp,sent)

            
    


if __name__==u"__main__":

    parser=Parser()
#    parser=Parser(u"full_model",test_time=True)
    
    for i in xrange(0,10):

        print >> sys.stderr, "iter",i+1
        parser.train(u"tdt.conll")
        break
        parser.perceptron_state.save(u"models/perceptron_model_"+str(i+1),retrainable=True)
    sys.exit()
    outf=codecs.open(u"parserout_test.conll",u"wt",u"utf-8")
    parser.parse(u"test.conll09",outf)
    outf.close()


