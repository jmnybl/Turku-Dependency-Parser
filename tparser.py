# -*- coding: utf-8 -*-

import time
import regressor_mlp
import numpy
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

from regressor import regressorWrapper, VRegressor
from reg import train
from collections import namedtuple

from auto_features import get_child

feats=Features()

SHIFT=0
RIGHT=1
LEFT=2
SWAP=3

DEPTYPES=u"acomp adpos advcl advmod amod appos aux auxpass ccomp compar comparator complm conj cop csubj csubj-cop dep det dobj gobj gsubj iccomp infmod intj mark name neg nommod nsubj num parataxis partmod poss prt punct rcmod voc xcomp xsubj xsubj-cop nsubj-cop nommod-own csubjpass nn cc number quantmod rel preconj ROOT".split() # TODO: collect these from data


#class Transition(object):

#    def __init__(self,move,dType=None):
#        self.move=move
#        self.dType=dType

#    def __eq__(self,other):
#        return self.move==other.move and self.dType==other.dType

#    def __str__(self):
#        return str(self.move)+":"+str(self.dType)

#    def __unicode__(self):
#        return unicode(self.move)+u":"+unicode(self.dType)

#    def __repr__(self):
#        return str(self.move)+":"+str(self.dType)
   

class State(object):

    def __init__(self,sent=None,syn=False,vector_len=20):
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
        self.wrong_transitions=0 # number of wrong transitions, if 0 then same as gold
        self.d_vectors=numpy.zeros((len(self.tree.tokens),vector_len)) #for every word its dependent role vector (filled in arc transition)
        self.g_vectors=numpy.zeros((len(self.tree.tokens),vector_len)) #for every word its governor role vector (accumulated when attaching its dependents)

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
        newS.d_vectors=s.d_vectors[:]
        newS.g_vectors=s.g_vectors[:]
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


    def update(self,move,d_type=None,d_vector=None,g_vector=None):
        if move==SHIFT: # SHIFT
            self.shift()
        elif move==RIGHT: # RIGHT ARC
            self.add_arc(self.stack[-2],self.stack.pop(-1),d_type=d_type,d_vector=d_vector,g_vector=g_vector) 
        elif move==LEFT: # LEFT ARC
            self.add_arc(self.stack[-1],self.stack.pop(-2),d_type=d_type,d_vector=d_vector,g_vector=g_vector)
        elif move==SWAP: # SWAP
            self.swap()
        else:
            raise ValueError("Incorrect transition")
        self.transitions.append(move)
        if len(self.queue)==0 and len(self.stack)==1:
            assert self.stack[-1].index==-1,("ROOT is not the last token in the stack.", self.stack)
            self.tree.ready=True


    def add_arc(self,gov,dep,d_type=None,d_vector=None,g_vector=None):
        """ Gov and dep are Token class instances. """
        dependency=Dep(gov,dep,d_type) #Note that d_type can be None at this point, in case we don't know what type we have
        self.tree.add_dep(dependency)
        if d_vector is not None:
            self.d_vectors[dep.index]=d_vector
        if g_vector is not None:
            self.g_vectors[gov.index]+=g_vector #accumulate the g_vectors

    def shift(self):
        self.stack.append(self.queue.pop(0))


    def swap(self):
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
        return (u"Tree ready? "+unicode(self.tree.ready)+u"\nStack: ["+u" ".join(token.text for token in self.stack)+u"]\nQueue: ["+u" ".join(token.text for token in self.queue)+u"]\nScore:"+unicode(self.score)+u"\n"+u"\n".join(u"("+dep.gov.text+u" "+dep.dep.text+u" "+unicode(dep.dType)+u")" for dep in self.tree.deps)).encode(u"utf-8")

    def __repr__(self):
        return u",".join(unicode(t.move)+u":"+unicode(t.dType) for t in self.transitions)


    def collect_tokens(self,move=None):
        ##move not needed anymore
        """ Tokens used to train regressor
            stack 1-3, queue 1-3, right 1-2 and left 1-2 dependent of stack 1-2 + leftmost of leftmost and rightmost of rightmost
            18 tokens + pos tags
        """
#        if move==LEFT:
        if len(self.stack)>0:
            g=self.stack[-1]
            tokens,pos,feat=self.fill_token(g,[],[],[]) # ...collect everything from gov token
        else:
            g=None
            tokens=[u"NONE"]*7
            pos=[u"NONE"]*7
            feat=[u"NONE"]*7
        if len(self.stack)>1:
            d=self.stack[-2]
            tokens,pos,feat=self.fill_token(d,tokens,pos,feat) # ...collect everything from dep token
        else:
            d=None
            for _ in range(7):
                tokens.append(u"NONE")
                pos.append(u"NONE")
                feat.append(u"NONE")

        # ...stack three
        if len(self.stack)>2 and self.stack[-3].text!=u"ROOT":
            tokens.append(self.stack[-3].text)
            pos.append(self.stack[-3].pos)
            feat.append(self.stack[-3].feat)
        else:
            tokens.append(u"NONE")
            pos.append(u"NONE")
            feat.append(u"NONE")

        # ...and queue
        for i in range(3):
            if len(self.queue)>i:
                tokens.append(self.queue[i].text)
                pos.append(self.queue[i].pos)
                feat.append(self.queue[i].feat)
            else:
                tokens.append(u"NONE")
                pos.append(u"NONE")
                feat.append(u"NONE")
        assert len(tokens)==len(pos) and len(tokens)==18, len(tokens)
        final=[]
        for i in range(len(tokens)):
            final.append(u"W:"+tokens[i])
            final.append(u"POS:"+pos[i])
            final.append(u"FEAT:"+feat[i])
            if pos[i]!=u"NONE" and feat[i]!=u"NONE":
                final.append(u"POS_FEAT:"+pos[i]+u"|"+feat[i])
            else:
                final.append(u"POS_FEAT:"+pos[i]+u"|"+u"NONE")
        return final

    def fill_token(self,token,tlist,plist,flist):
        tlist.append(token.text)
        plist.append(token.pos)
        flist.append(token.feat)
        # left and rightmost dependents + leftmost of leftmost and rightmost of rightmost
        childs=sorted(self.tree.childs[token], key=lambda x:x.index)
        if len(childs)>0:
            if childs[0].index<token.index: # leftmost
                tlist.append(childs[0].text)
                plist.append(childs[0].pos)
                flist.append(childs[0].feat)
                dep_childs=sorted(self.tree.childs[childs[0]], key=lambda x:x.index)
                if len(dep_childs)>0 and dep_childs[0].index<childs[0].index: # leftmost of leftmost
                    tlist.append(dep_childs[0].text)
                    plist.append(dep_childs[0].pos)
                    flist.append(dep_childs[0].feat)
                else:
                    tlist.append(u"NONE")
                    plist.append(u"NONE")
                    flist.append(u"NONE")
                if len(childs)>2 and childs[1].index<token.index: # second leftmost
                    tlist.append(childs[1].text)
                    plist.append(childs[1].pos)
                    flist.append(childs[1].feat)
                else:
                    tlist.append(u"NONE")
                    plist.append(u"NONE")
                    flist.append(u"NONE")
            else:
                for _ in range(3):
                    tlist.append(u"NONE")
                    plist.append(u"NONE")
                    flist.append(u"NONE")
            if childs[-1].index>token.index: # rightmost
                tlist.append(childs[-1].text)
                plist.append(childs[-1].pos)
                flist.append(childs[-1].feat)
                dep_childs=sorted(self.tree.childs[childs[-1]], key=lambda x:x.index)
                if len(dep_childs)>0 and dep_childs[-1].index>childs[-1].index: # rightmost of rightmost
                    tlist.append(dep_childs[-1].text)
                    plist.append(dep_childs[-1].pos)
                    flist.append(dep_childs[-1].feat)
                else:
                    tlist.append(u"NONE")
                    plist.append(u"NONE")
                    flist.append(u"NONE")
                if len(childs)>2 and childs[-2].index>token.index: # second rightmost
                    tlist.append(childs[-2].text)
                    plist.append(childs[-2].pos)
                    flist.append(childs[-2].feat)
                else:
                    tlist.append(u"NONE")
                    plist.append(u"NONE")
                    flist.append(u"NONE")
            else:
                for _ in range(3):
                    tlist.append(u"NONE")
                    plist.append(u"NONE")
                    flist.append(u"NONE")
        else:
            for _ in range(6):
                tlist.append(u"NONE")
                plist.append(u"NONE")
                flist.append(u"NONE")
        return tlist,plist,flist

class Parser(object):


    def __init__(self,model_file_name,regressor,fName=None,gp=None,beam_size=5,test_time=False):
        self.test_time=test_time
        self.features=Features()
        self.beam_size=beam_size
        self.model=Model.load(model_file_name)
        self.regressor=regressor


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
                gs_transitions=self.extract_transitions(gs_tree,sent) #gs_transitions is a list of (move,dtype) tuples
                self.train_one_sent(gs_transitions,sent,progress) # sent is a conll sentence
            except ValueError:
                traceback.print_exc()
                failed+=1 
        if not quiet:
            print u"Failed to parse:",failed
            print u"Total number of trees:",total
            print u"Non-projectives:",non
            print u"Progress:",progress

    def collect_train_data(self,inp,out):

        print >> sys.stderr, "...collecting training data for regression"

        for sent in read_conll(inp):
            try:
                tree=Tree.new_from_conll(conll=sent,syn=True)
                non_projs=tree.is_nonprojective()
                if len(non_projs)>0:
                    tree.define_projective_order(non_projs)

                state=State(sent,syn=False)
                while not state.tree.ready:
                    if len(state.queue)==0 and len(state.stack)==2:
                        break
                    if len(state.stack)>1:
                        move,dtype=self.extract_dep(state,tree)
                        if move is not None:
                            if move not in state.valid_transitions():
                                raise ValueError("Invalid transition:",move)
                            reg_tokens=state.collect_tokens(move)
                            print >> out, move, dtype, (u" ".join(t for t in reg_tokens)).encode(u"utf-8")
                            # now collect tokens for regressor training
#                            reg_tokens=state.collect_tokens(move)
#                            print >> out, dtype, (u" ".join(t for t in reg_tokens)).encode(u"utf-8")

                            state.update(move,dtype)
                            continue


                    if (len(state.stack)>1) and (tree.projective_order is not None) and (state.stack[-2].index<state.stack[-1].index) and (tree.is_proj(state.stack[-2],state.stack[-1])): # SWAP
                        move=SWAP
                    else: # SHIFT
                        move=SHIFT
                    reg_tokens=state.collect_tokens(move)
                    print >> out, move, u"None", (u" ".join(t for t in reg_tokens)).encode(u"utf-8")

                    state.update(move)
            except:
                traceback.print_exc()
                print >> sys.stderr, "FAIL"

        print >> sys.stderr, "...done"

        



    def extract_transitions(self,gs_tree,sent):
        state=State(sent,syn=False)
        trans_seq=[]
        while not state.tree.ready:
            if len(state.queue)==0 and len(state.stack)==2: # only final ROOT arc needed (it's not part of a tree)
                move,=state.valid_transitions() # this is used to decide whether we need LEFT or RIGHT
                assert (move==RIGHT or move==LEFT)
                state.update(move,u"ROOT")
                trans_seq.append((move,u"ROOT"))
                continue
            if len(state.stack)>1:
                move,dtype=self.extract_dep(state,gs_tree)
                if move is not None:
                    if move not in state.valid_transitions():
                        raise ValueError("Invalid transition:",move)
                    state.update(move,dtype)
                    trans_seq.append((move,dtype))
                    continue
            # cannot draw arc
            if (len(state.stack)>1) and (gs_tree.projective_order is not None) and (state.stack[-2].index<state.stack[-1].index) and (gs_tree.is_proj(state.stack[-2],state.stack[-1])): # SWAP
                    move=SWAP
            else: # SHIFT
                move=SHIFT
            if move not in state.valid_transitions():
                raise ValueError("Invalid transition:",move)
            state.update(move)
            trans_seq.append((move,None))
        return trans_seq
            
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
        beam=[State(sent,syn=False,vector_len=self.regressor.hidden_dep.n_out)] # create an 'empty' state, use sent (because lemma+pos+feat), but do not fill syntax      
        gs_state=State(sent,syn=False,vector_len=self.regressor.hidden_dep.n_out)
        while not self.beam_ready(beam):
            if not gs_state.tree.ready: # update gs if it's not ready
                move,dtype=gs_transitions[len(gs_state.transitions)]
                if move not in gs_state.valid_transitions():
                    raise ValueError("Invalid GS Transition")
                #s=self.perceptron.score(gs_state.features,False,prefix=unicode(move))
                #gs_state=State.copy_and_point(gs_state) #okay, this we could maybe avoid TODO @fginter
                #gs_state.score+=s
                
                if move==RIGHT or move==LEFT:
                    if len(gs_state.queue)==0 and len(gs_state.stack)==2: 
                        dtype=u"ROOT"

                gs_state.update(move,dtype)
                #gs_state.features=feats.create_features(gs_state)
            else:
                move,dtype=None,None

            beam=self.give_next_state(beam,move,dtype) # update beam TODO    

            best_state=beam[0]
#            if len(beam)>1:
#                state2nd=beam[1]
#            else:
#                state2nd=None

            if not self.gold_in_beam(beam): # check if gold state is still in beam
                prog=float(len(best_state.transitions))/len(gs_transitions)
                print "%.01f%%     %d/%d  "%(prog*100.0,len(best_state.transitions),len(gs_transitions))
                sys.stdout.flush()
                ###self.perceptron.update(best_state.create_feature_dict(),gs_state.create_feature_dict(),best_state.score,gs_state.score,best_state.wrong_transitions,progress) # update the perceptron
                break
        else: # gold still in beam and beam ready
            if beam[0].wrong_transitions==0: # no need for update
                print "**", len(gs_state.transitions)
            else:
                #self.perceptron.update(beam[0].create_feature_dict(),gs_state.create_feature_dict(),beam[0].score,gs_state.score,beam[0].wrong_transitions,progress) # update the perceptron
                print "*", len(gs_state.transitions)
        #Done with the example, update the average vector
        #self.perceptron.add_to_average()


    def enum_transitions(self,state):
        """Enumerates transition objects allowable for the state. TODO: Filtering here?"""
        for move in state.valid_transitions():
            yield move
                
    def beam_ready(self,beam):
        for state in beam:
            if not state.tree.ready: return False
        return True

    def gold_in_beam(self,beam):
        for state in beam:
            if state.wrong_transitions==0: return True
        return False

    def give_next_state(self,beam,gs_move=None,gs_dtype=None):
        """ Predict next state and creates it. Also returns the next best state, needed for the margin update """
        #We want to
        # 1) go over the allowed transitions and score each state with that operation's prefix
        # 2) apply the next transition

        if len(beam)>self.beam_size:
            raise ValueError("Beam too big!") # ...for dev time only, to make sure we update the beam correctly

        #Rank the state w.r.t. every possible transition, use str(trans) as the prefix to differentiate features
        scores=[] #Holds (score,transition,state) tuples
        feats=[] #features of the states to be evaluated in a minibatch
        states=[] #the states in a minibatch
        for state in beam:
            if len(state.queue)==0 and len(state.stack)==1: # this state is ready
                scores.append((state.score,None,state))
                continue
            feats.append(state.collect_tokens())
            states.append(state)
#            print "len feats", len(feats[-1])
        reg_input=self.regressor.features_to_input(feats)
        reg_scores=self.regressor.test_scores_move(reg_input)
        print "feats"
        print feats
        print "len(states)", len(states)
        print "reg input. shape=", reg_input.shape
        print reg_input
        print "reg scores. shape=", reg_scores.shape
        print reg_scores
        print
        print
        assert len(states)==len(feats) and reg_scores.shape[0]==len(states)
        for s_idx, state in enumerate(states):
            for move in self.enum_transitions(state):
                scores.append((reg_scores[s_idx,move],move,state))
            
            # for move in self.enum_transitions(state):
            #     s=self.regressor.score(state)
            #     scores.append((state.score+s,move,state))
        #Okay, now we have the possible continuations ranked
        selected_transitions=sorted(scores, reverse=True)[:self.beam_size] # now we have selected the new beam, next update states

        new_beam=[]
        for score,move,state in selected_transitions:
           # print score, move
            #For each of these, we will now create a new state and build its features while we are at it, because now is the time to do it efficiently
            if move is None: # this state is ready
                new_beam.append(state)
                continue
            newS=State.copy_and_point(state)

            if move==RIGHT or move==LEFT:
                if len(state.queue)==0 and len(state.stack)==2: # must be ROOT
                    dtype=u"ROOT"
                else:
                    #dtype=u"xxx" ## TODO: regress the type
                    if move==LEFT:
                        tokens=[state.stack[-2].text,state.stack[-1].text]
                    else:
                        tokens=[state.stack[-1].text,state.stack[-2].text]
                newS.update(move,d_type=u"xxx")
            else:
                newS.update(move)

            newS.score=score # Do not use '+'
            #if (gs_trans is None) or (not transition==gs_trans):
            if (gs_move is None) or (gs_move!=move): # TODO: ignore deptype
                newS.wrong_transitions+=1 # TODO: is this fair?
#            newS.features,factors=feats.create_general_features(newS)
#            newS.features.update(feats.create_deptype_features(newS,factors))
            new_beam.append(newS)
        return new_beam #List of selected states, ordered by their score in this move


    def parse(self,inp,outp):
        """outp should be a file open for writing unicode"""
        sent_counter=0
        token_counter=0
        beg=time.time()
        for sent in read_conll(inp):
            sent_counter+=1
            token_counter+=len(sent)
            beam=[State(sent,syn=False)]
            while not self.beam_ready(beam):
                beam=self.give_next_state(beam) #This looks wasteful, but it is what the beam will do anyway
            fill_conll(sent,beam[0])
            write_conll(outp,sent)
        end=time.time()
        ms=end*1000.0-beg*1000.0
        print >> sys.stderr, "Parsed %d trees %d tokens in %d seconds (without startup cost)"%(sent_counter,token_counter,int(end-beg))
        print >> sys.stderr, "%.1f ms/tree, %.1f trees/sec, %.1f tokens/sec"%(ms/sent_counter,sent_counter/(end-beg),token_counter/(end-beg))
        print >> sys.stderr

            
    


if __name__==u"__main__":


    # ## just to collect regressor traindata
    # parser=Parser(u"corpus_stats.pkl",None,beam_size=5)
    # parser.collect_train_data(codecs.getreader(u"utf-8")(sys.stdin),codecs.getreader(u"utf-8")(sys.stdout))
    # sys.exit()


    # # ...HACK TO TRAIN REGRESSOR...

    # vr=VRegressor(600,10)
    
    # #reg.train needs these arguments
    # arguments=namedtuple("arg_names",["wvtoken","wvmorpho","conll09","dtype","morpho"])
    # values={"val1":arguments("/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin","vectors.dtype.tdtjk.bin",True,True,False)}
    # temp_args=values["val1"]
    
    # train(temp_args,vr,0.01)
    
    # reg_wrapper=regressorWrapper("/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin","vectors.dtype.tdtjk.bin",vr)

    # parser=Parser(u"corpus_stats.pkl",reg_wrapper,beam_size=5)
    
    # for i in xrange(0,10):

    #     print >> sys.stderr, "iter",i+1
    #     parser.train(u"tdt-train-jktagged.conll09")
    #     break
    #     parser.perceptron_state.save(u"models/perceptron_model_"+str(i+1),retrainable=True)
    # sys.exit()
    regressor=regressor_mlp.MLP_WV.load("cls8386")
    parser=Parser(u"corpus_stats.pkl",regressor,beam_size=5)
    parser.test_time=True
    outf=codecs.open(u"parsed.xxx.conll",u"wt",u"utf-8")
    parser.parse(u"data/fi-ud-dev-mmtagged.conllu",outf)
    outf.close()


