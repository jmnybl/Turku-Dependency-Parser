# -*- coding: utf-8 -*-

import datetime
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

    def __unicode__(self):
        return unicode(self.move)+u":"+unicode(self.dType)

    def __repr__(self):
        return str(self.move)+":"+str(self.dType)
   

class State(object):

    def __init__(self,sent=None):
        if sent!=None:
            self.tree,self.extra_tree=Tree.new_from_conll(sent)
        else:
            self.tree,self.extra_tree=None,None
        self.extra_tree.create_routes()
        #Not today   <- huh? TODO
        #self.extra_tree.create_context_routes()
        self.stack=[]
        self.queue=self.extra_tree.BFS_queue(self.tree.tokens[self.tree.semeval_root_idx])
        self.stack.extend(self.queue[:2]) #Put the first two tokens on the stack, should be semeval_root_idx and the first word
        assert self.stack[-2].is_semeval_root==True
        self.queue[:2]=[]
        self.score=0.0
        self.transitions=[]
        self.features=defaultdict(lambda:0.0)
        self.prev_state=None #The state from which this one was created, if any
        self.wrong_transitions=0 # number of wrong transitions, if 0 then same as gold

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
        newS.transitions=s.transitions[:] # TODO: we don't need the whole sequence anymore, just last 4 for feature generation
        newS.prev_state=s
        newS.wrong_transitions=s.wrong_transitions
        #newS.tree=copy.deepcopy(s.tree)
        newS.tree=Tree.new_from_tree(s.tree) ###MUST get rid of token.dtype first
        newS.extra_tree=s.extra_tree
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
                if f.startswith(u"grf"):
                    d[f]=d.get(f,0.0)+w
                else:
                    d[prefix+f]=d.get(f,0.0)+w
        if self.prev_state:
            self.prev_state._populate_feature_dict(d,unicode(self.transitions[-1])) #Use the last transition as the prefix for the state which resulted in this one

    def update(self,trans):
        if trans.move==RIGHT: # RIGHT ARC + SHIFT
            assert self.stack[-2].is_semeval_root
            self.add_arc(self.stack[-2],self.stack.pop(-1),trans)
            if len(self.queue)>0:
                self.stack.append(self.queue.pop(0))
        else:
            raise ValueError("Incorrect transition")
        self.transitions.append(trans)
        if len(self.queue)==0 and len(self.stack)==1:
            assert self.stack[-1].is_semeval_root,("semeval is not the last token in the stack.", self.stack)
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
        if len(self.stack)==2:
            assert self.stack[-2].is_semeval_root
            moves.add(RIGHT)
        return moves

    def __str__(self):
        return (u"Tree ready? "+unicode(self.tree.ready)+u"\nStack: ["+u" ".join(token.text for token in self.stack)+u"]\nQueue: ["+u" ".join(token.text for token in self.queue)+u"]\nScore:"+unicode(self.score)+u"\n"+u"\n".join(u"("+dep.gov.text+u" "+dep.dep.text+u" "+dep.dType+u")" for dep in self.tree.deps)).encode(u"utf-8")

    def __repr__(self):
        return u",".join(str(t.move)+u":"+str(t.dType) for t in self.transitions)


class Parser(object):


    def __init__(self,fName=None,gp=None,beam_size=40,test_time=False):
        self.test_time=test_time
        self.features=Features()
        self.beam_size=beam_size
        if os.path.exists(u"corpus_stats_dm.pkl"):
            self.model=Model.load(u"corpus_stats_dm.pkl")
        else:
            self.model=Model.collect(u"corpus_stats_dm.pkl",u"semeval_data/train_dm_trees.conll")
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
        for sidx, (sent,comments) in enumerate(read_conll(inp)):
            total+=1
            gs_tree,e=Tree.new_from_conll(sent,extra_tree=False) # extra_tree is always False here, no need for it yet
            gs_tree.fill_syntax(sent)
            non_projs=gs_tree.is_nonprojective()
            if len(non_projs)>0:
                gs_tree.define_projective_order(non_projs)
                non+=1
            try:
                gs_transitions=self.extract_transitions(gs_tree,sent)
                self.train_one_sent(gs_transitions,sent,progress) # sent is a conll sentence
            except ValueError:
                traceback.print_exc()
                failed+=1
            except:
                print >> sys.stderr, "ERROR! ERROR!"
                print >> sys.stderr, repr(sent)
                print >> sys.stderr, "End of repr"
                traceback.print_exc()
        if not quiet:
            print datetime.datetime.now().isoformat()
            print u"Failed to parse:",failed
            print u"Total number of trees:",total
            print u"Non-projectives:",non
            print u"Progress:",progress


    def extract_transitions(self,gs_tree,sent):
        state=State(sent)
        #print state.queue
        while not state.tree.ready:
##            if len(state.queue)==0 and len(state.stack)==2: # only final ROOT arc needed (it's not part of a tree)
##                move,=state.valid_transitions() # this is used to decide whether we need LEFT or RIGHT
##                assert (move==RIGHT or move==LEFT)
##                trans=Transition(move,u"ROOT") # TODO semeval 
##                state.update(trans)
##                continue
            g,d=state.stack[-2],state.stack[-1]
            dType=gs_tree.has_dep(g,d)
            assert dType is not None
            trans=Transition(RIGHT,dType)
            state.update(trans)
        assert len(state.transitions)==len(state.tree.tokens)-1
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
        beam=[State(sent)] # create an 'empty' state, use sent (because lemma+pos+feat), but do not fill syntax      
        beam[0].features=feats.create_features(beam[0]) #Added this one here because otherwise the update would have no features to work with
        gs_state=State(sent)
        gs_state.features=feats.create_features(gs_state) #Added this one here because the first transition should have some features to work with
        #print "context:",gs_state.extra_tree.context
        #print "routes:",gs_state.extra_tree.routes
        while not self.beam_ready(beam):
            if not gs_state.tree.ready: # update gs if it's not ready
                gs_trans=gs_transitions[len(gs_state.transitions)]
                if gs_trans.move not in gs_state.valid_transitions():
                    raise ValueError("Invalid GS Transition")
                s=self.perceptron.score(gs_state.features,False,prefix=unicode(gs_trans))
                gs_state=State.copy_and_point(gs_state) #okay, this we could maybe avoid TODO @fginter
                gs_state.score+=s
                gs_state.update(gs_trans)
                gs_state.features=feats.create_features(gs_state)
            else:
                assert False
                gs_trans=None

            beam=self.give_next_state(beam,gs_trans) # update beam         

            best_state=beam[0]
#            if len(beam)>1:
#                state2nd=beam[1]
#            else:
#                state2nd=None

            if not self.gold_in_beam(beam): # check if gold state is still in beam
                prog=float(len(best_state.transitions))/len(gs_transitions)
                print "%.01f%%     %d/%d  "%(prog*100.0,len(best_state.transitions),len(gs_transitions))
                sys.stdout.flush()
                self.perceptron.update(best_state.create_feature_dict(),gs_state.create_feature_dict(),best_state.score,gs_state.score,best_state.wrong_transitions,progress) # update the perceptron
                break
#            elif state2nd is not None and best_state.score-state2nd.score<1.0: #Prediction OK, but no margin
#                print "+", len(best_state.transitions)
#                #Update and continue training...
#                self.perceptron.update(state2nd.create_feature_dict(),best_state.create_feature_dict(),state2nd.score,best_state.score,progress)
        else: # gold still in beam and beam ready
            if beam[0].wrong_transitions==0: # no need for update
                print "**", len(gs_state.transitions)#, gs_state.transitions
            else:
                self.perceptron.update(beam[0].create_feature_dict(),gs_state.create_feature_dict(),beam[0].score,gs_state.score,beam[0].wrong_transitions,progress) # update the perceptron
                print "*", len(gs_state.transitions)
        #Done with the example, update the average vector
        self.perceptron.add_to_average()


    def enum_transitions(self,state):
        """Enumerates transition objects allowable for the state. TODO: Filtering here?"""
        for move in state.valid_transitions():
            if move==RIGHT:
                if move==RIGHT:
                    gov_pos=state.stack[-2].pos
                    dep_pos=state.stack[-1].pos
                else:
                    assert False
                allowed=self.model.deptypes.get((gov_pos,dep_pos),set())
                allowed.add(u"NOTARG")
                for dType in allowed:
                    yield Transition(move,dType)
            else:
                assert False
                


    def beam_ready(self,beam):
        for state in beam:
            if not state.tree.ready: return False
        return True

    def gold_in_beam(self,beam):
        for state in beam:
            if state.wrong_transitions==0: return True
        return False



    def give_next_state(self,beam,gs_trans=None):
        """ Predict next state and creates it. Also returns the next best state, needed for the margin update """
        #We want to
        # 1) go over the allowed transitions and score each state with that operation's prefix
        # 2) apply the next transition

        if len(beam)>self.beam_size:
            raise ValueError("Beam too big!") # ...for dev time only, to make sure we update the beam correctly

        #Rank the state w.r.t. every possible transition, use str(trans) as the prefix to differentiate features
        scores=[] #Holds (score,transition,state) tuples
        for state in beam:
            if len(state.queue)==0 and len(state.stack)==1: # this state is ready
                scores.append((state.score,None,state))
                continue
            for trans in self.enum_transitions(state):
                s=self.perceptron.score(state.features,self.test_time,prefix=unicode(trans))
                scores.append((state.score+s,trans,state))
        #Okay, now we have the possible continuations ranked
        selected_transitions=sorted(scores, key=lambda s: s[0], reverse=True)[:self.beam_size] # now we have selected the new beam, next update states

        new_beam=[]
        for score,transition,state in selected_transitions:
            #For each of these, we will now create a new state and build its features while we are at it, because now is the time to do it efficiently
            if transition is None: # this state is ready
                new_beam.append(state)
                continue
            newS=State.copy_and_point(state)
            newS.update(transition)
            newS.score=score # Do not use '+'
            if (gs_trans is None) or (not transition==gs_trans):
                newS.wrong_transitions+=1 # TODO: is this fair? (TODO2: what do you mean here, @jmnybl?)
            newS.features,factors=feats.create_general_features(newS)
            newS.features.update(feats.create_deptype_features(newS,factors))
            new_beam.append(newS)
        return new_beam #List of selected states, ordered by their score in this move



    def parse(self,inp,outp):
        """outp should be a file open for writing unicode"""
        for sent,comments in read_conll(inp):
            if len(sent)==1:
                write_conll(outp,sent,comments)
                continue
            beam=[State(sent)]
            beam[0].features=feats.create_features(beam[0])
            while not self.beam_ready(beam):
                beam=self.give_next_state(beam) #This looks wasteful, but it is what the beam will do anyway
            fill_conll(sent,beam[0])
            write_conll(outp,sent,comments)

            
    


if __name__==u"__main__":

    parser=Parser()
#    parser=Parser(u"full_model",test_time=True)
    
    for i in xrange(0,10):

        print >> sys.stderr, "iter",i+1
        #parser.train(u"tdt.conll")
        parser.train(u"semeval_data/train_dm_trees.conll")
        break
        parser.perceptron_state.save(u"models/perceptron_model_"+str(i+1),retrainable=True)
    sys.exit()
    outf=codecs.open(u"parserout_test.conll",u"wt",u"utf-8")
    parser.parse(u"test.conll09",outf)
    outf.close()


