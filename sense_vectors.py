# -*- coding: utf-8 -*-


from seval2tree import get_sentence
from top_nodes import get_full_sentence

import sys

from collections import defaultdict

import numpy as np
from wvlib import wvlib

import cPickle as pickle
import codecs
import os.path
import glob
import argparse


def collect_tokens(token_id, sent, arguments):
    """ Takes a predicate and a sentence, and returns a list of tokens we should use to build the average vetor.
        token_id is 0-based
        arguments: key: gov, value: set of of (dep, role)
    """
    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

    # collect syntax
    syntax_heads={} # key: token id, value: (head,deprel) (...I could create this only once...)
    syntax_deps=defaultdict(lambda:[]) # key: token id, value: list of (dep id, deprel) tuples
    for line in sent:
        if line[DEPS]!=u"_": # syntax
            g,t=line[DEPS].split(u":")
            syntax_heads[int(line[ID])]=(int(g),t) # head
            syntax_deps[int(g)].append((int(line[ID]),t)) # collect deps
    
    tokens=[]
    
    # governor
    g,t=syntax_heads[token_id+1]
    if g==0:
        rel=u"root"
    else:
        rel=syntax_heads[g][1]
    tokens.append((sent[g-1][TOKEN],rel))

    # dependents
    for d,t in syntax_deps[token_id+1]:
        tokens.append((sent[d-1][TOKEN],t))

    # semantic gov+deps
    for key, val in arguments.iteritems():
        for d,r in val:
            if key==token_id+1:
                tokens.append((sent[d-1][TOKEN],u"sem-"+r))
            elif d==token_id+1:
                tokens.append((sent[key-1][TOKEN],u"sem-"+r))
    

    return tokens

        
def calculate_average(tokens,deprels,mapping):

    avg_vector=None
    for token,dep in tokens:
        if dep not in deprels:
            print >> sys.stderr, "No shift for", dep
            continue
        vec=mapping[token]
        vec=np.roll(vec,deprels.index(dep))
        if avg_vector is None:
            avg_vector=vec
        else:
            avg_vector+=vec
    if avg_vector is None:
        return np.zeros(300,np.int32)
    return avg_vector/len(tokens)


def train(wv_model,model_name):
    """
    Trains a 'something' to predict senses.
    Uses .conllu format.
    """
    
    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

    model=wvlib.load(wv_model, max_rank=600000).normalize()
    mapping=model.word_to_vector_mapping()


    senses=defaultdict(lambda:set())
    train_examples=defaultdict(lambda:[])

    deprels=set()

    for comments,sentences,arguments in get_full_sentence(codecs.getreader(u"utf-8")(sys.stdin)):

        # collect syntax
        syntax_heads={} # key: token id, value: (head,deprel) (...I could create this only once...)
        syntax_deps=defaultdict(lambda:[]) # key: token id, value: list of (dep id, deprel) tuples
        for line in sentences[0]:
            if line[DEPS]!=u"_": # syntax
                g,t=line[DEPS].split(u":")
                deprels.add(t)
                syntax_heads[int(line[ID])]=(int(g),t) # head
                syntax_deps[int(g)].append((int(line[ID]),t)) # collect deps

        for key,val in arguments.iteritems(): # val is set
            for k,arg in val:
                deprels.add(u"sem-"+arg)


        for i in xrange(len(sentences[0])): # each sentence has the required information, so we can take just the first one
            
            if u"SENSE=" not in sentences[0][i][MISC]:
                continue

            sense=None
            for item in sentences[0][i][MISC].split(u"|"):
                if item.startswith(u"SENSE="):
                    sense=item.split(u"=",1)[1]
                    break
            assert sense is not None

            key=u"_".join([sentences[0][i][LEMMA],sentences[0][i][POS]])

            tokens=collect_tokens(i,sentences[0],arguments)

            existing_tokens=[(t,rel) for t,rel in tokens if t in mapping]

            senses[key].add(sense)

            train_examples[(key,sense)]+=existing_tokens

    one_sense={}
    multi_senses={}
    for key,value in senses.iteritems():
        if len(value)==1:
            one_sense[key]=list(value)[0]
        else:
            multi_senses[key]=value

    # if lemma+pos has only one sense, just store it
    print 'Saving models'

    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    f=codecs.open(os.path.join(model_name,u"one_sense.pkl"),u"wb")
    pickle.dump(one_sense,f)
    f.close()

    # train vector stuff
    print 'Average vectors...'
    vocab=codecs.open(os.path.join(model_name,u"vocab.txt"),u"wt",u"utf-8")
    vect_model=codecs.open(os.path.join(model_name,u"avg_vectors.npy"),u"wb")

    # args set is the list of all roles
    deprel_list=sorted(deprels)

    for key,senses in multi_senses.iteritems():
        for sense in senses:
            tokens=train_examples[(key,sense)]
            if len(tokens)>0:
                avg_vector=calculate_average(tokens,deprel_list,mapping)
                print >> vocab, key, sense
                avg_vector.tofile(vect_model)

    vocab.close()
    vect_model.close()

    with codecs.open(os.path.join(model_name,u"deprels.pkl"),u"wb") as f:
        pickle.dump(deprel_list,f)
    

    
def predict(wv_model,model_name):

    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)
    out=codecs.getwriter(u"utf-8")(sys.stdout)

    model=wvlib.load(wv_model, max_rank=600000).normalize()
    mapping=model.word_to_vector_mapping()

    directory=model_name.rsplit(u"/",1)[0]

    # load one_sense dictionary
    with codecs.open(os.path.join(directory,u"one_sense.pkl"),u"rb") as f:
        one_sense=pickle.load(f)

    ## load tokens + average matrix
    with codecs.open(os.path.join(directory,u"vocab.txt"),u"r",u"utf-8") as f:
        vocab=[t.rstrip(u"\n") for t in f]

    # load deprels (to get shifts)
    with codecs.open(os.path.join(directory,u"deprels.pkl"),u"rb") as f:
        deprel_list=pickle.load(f)


    senses={}
    for line in vocab:
        key,sense=line.split()
        if key not in senses:
            senses[key]=set()
        senses[key].add(sense)    

    vect_model=np.fromfile(os.path.join(directory,u"avg_vectors.npy"),np.float32,-1)

    vect_model=vect_model.reshape(vect_model.shape[0]/300,300)


    for comments,sentences,arguments in get_full_sentence(codecs.getreader(u"utf-8")(sys.stdin)):
    
        predictions={}

        for i in xrange(len(sentences[0])): # each sentence has the required information, so we can take just the first one
            
            key=u"_".join([sentences[0][i][LEMMA],sentences[0][i][POS]])

            if key in one_sense:
                predictions[i]=one_sense[key]
                continue
            if key in senses:

                tokens=collect_tokens(i,sentences[0],arguments)
                existing_tokens=[(t,rel) for t,rel in tokens if t in mapping]
                if len(existing_tokens)==0:
                    continue
                avg_vector=calculate_average(existing_tokens,deprel_list,mapping)

                max_score=None
                max_sense=None

                for sense in senses[key]:

                    idx=vocab.index(u" ".join([key,sense]))
                    sense_vector=vect_model[idx]

                    sim=model.similarity(sense_vector,avg_vector)
                    if max_score is None or sim>max_score:
                        max_score=sim
                        max_sense=sense

                predictions[i]=max_sense
     


        # print sentences out with top node predictions
        for i in xrange(len(sentences)):
            comment=comments[i]
            sent=sentences[i]
            print >> out, comment
            for idx,line in enumerate(sent):
                if idx in predictions:
                    if line[MISC]==u"_":
                        line[MISC]=u"SENSE="+predictions[idx]
                    else:
                        line[MISC]=line[MISC]+u"|SENSE="+predictions[idx]
                print >> out, u"\t".join(c for c in line)
            print >> out




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Sense prediction.')
    g=parser.add_argument_group("")
    g.add_argument('--model', required=True, help='Name of the model.')
    g.add_argument('--train', required=False, action="store_true", default=False, help='Train prediction from stdin.')
    g.add_argument('--predict', required=False, action="store_true", default=False, help='Predict senses.')
    g.add_argument('--wv', required=True, help='Word2vec model')
    args = parser.parse_args()

    if args.train:
        train(args.wv, args.model) # wv model, model to be trained
    elif args.predict:
        predict(args.wv,args.model)
    else:
        print >> sys.stderr, "Train or predict?"
        sys.exit(1)

###############################



    
