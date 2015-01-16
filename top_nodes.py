from seval2tree import get_sentence
import sys

from collections import defaultdict

from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

import cPickle as pickle
import codecs
import os.path
import glob
import argparse


def get_full_sentence(f):

    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

    comments=[]
    sentences=[]
    arguments={}
    
    for comment,sent in get_sentence(f):

        if not sent: # this is empty sentence
            assert u"." not in comment
            yield comments,sentences,arguments # yield last one
            comments=[]
            sentences=[]
            arguments={}
            comments.append(comment) # add only comment
            continue

        idx,count=comment.rsplit(u".",1)
        count=int(count)
        if count==0: # new sentence
            if comments:
                yield comments, sentences, arguments
            comments=[]
            sentences=[]
            arguments={}
        comments.append(comment)
        sentences.append(sent)
        # collect arguments
        for line in sent:
            if line[DEPREL]!=u"NOTARG" and line[DEPREL]!=u"ROOT":
                if int(line[HEAD]) not in arguments:
                    arguments[int(line[HEAD])]=set()
                arguments[int(line[HEAD])].add((int(line[ID]),line[DEPREL]))    
    if comments:
        yield comments, sentences, arguments

def polynomial_features(feats):
    """ Every feature value is just 1.0 so feats is just a list of features, not really a dictionary..."""
    final_features={}
    flist=[]
    for fname, val in feats.iteritems():
        flist.append(fname)
    flist.sort()
    for i in xrange(0,len(flist)):
        for j in xrange(i,len(flist)):
            f1=flist[i]
            f2=flist[j]
            final_features[f1+f2] = 1.0
    return final_features

def create_features(token_id, sent, args):
    """ token_id is 0-based, args keys are 1-based ints"""
    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

    features=defaultdict(float)

    syntax_heads={} # key: token id, value: (head,deprel) (...I could create this only once...)
    syntax_deps=defaultdict(lambda:[]) # key: token id, value: list of (dep id, deprel) tuples
    for line in sent:
        if line[DEPS]!=u"_": # syntax
            g,t=line[DEPS].split(u":")
            syntax_heads[int(line[ID])]=(int(g),t) # head
            syntax_deps[int(g)].append((int(line[ID]),t)) # collect deps

    features[u"deprel=%s" % syntax_heads[token_id+1][1]] = 1.0 # deprel
    features[u"pos=%s" % sent[token_id][POS]] = 1.0 # pos
    features[u"lemma=%s" % sent[token_id][LEMMA]] = 1.0 # lemma

    # semantic roles (...I should do this only once...)
    for key,value in args.iteritems():
        for token,role in value:
            if token==token_id+1:
                features[u"role=%s" % role] = 1.0

                # semantic siblings
                for dep,r in args[key]:
                    if dep!=token:
                        features[u"semantic_sibling=%s" % r] = 1.0
    
    # is predicate
    if  token_id+1 in args:
        features["predicate=yes"] = 1.0

        # args (ie. semantic dependents)
        for arg,role in args[token_id+1]:
            features[u"arg=%s" % role] = 1.0

    # syntactic dependents
    for d,t in syntax_deps[token_id+1]:
        features[u"syntactic_dep=%s" % t] = 1.0

    # syntactic governor lemma
    g,t=syntax_heads[token_id+1]
    if g!=0: # not root
        features[u"syntax_gov_lemma=%s" % sent[g-1][LEMMA]] = 1.0

    # syntactic siblings
    for dep,t in syntax_deps[g]:
        if dep!=token_id+1:
            features[u"syntactic_sibling=%s" % t] = 1.0

    return polynomial_features(features)


def get_label(token_id, sent):
    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)
    if u"TOPNODE=Yes" in sent[token_id][MISC]:
        return 1
    else:
        return 0


def train(model_name):
    """
    Trains a classifier to predict top nodes.
    Uses .conllu format, where each sentence is one training example (is root top node?).
    """
    vectorizer = DictVectorizer()
    train_examples=[]
    train_labels=[]

    for comments,sentences,arguments in get_full_sentence(codecs.getreader(u"utf-8")(sys.stdin)):

        if not sentences:
            continue

        for i in xrange(len(sentences[0])): # each sentence has the required information, so we can take just the first one
            
            train_examples.append(create_features(i,sentences[0],arguments))
            train_labels.append(get_label(i,sentences[0]))

    pos,neg=0,0
    for label in train_labels:
        if label==1:
            pos+=1
        elif label==0:
            neg+=1
        else:
            assert False

    print "Training data has %d positive examples and %d negative examples" % (pos,neg)

    train_examples = vectorizer.fit_transform(train_examples)
    
    print "Training data has %s examples and %s features" % (train_examples.shape)
    
    print "Training classifiers"
    
    c_values = [2**i for i in range(-5, 15)]
    
    classifiers = [LinearSVC(C=c, random_state=1) for c in c_values]
    
    for idx, classifier in enumerate(classifiers):
        print 'Training classifier %s with C value %s' % (idx,classifier.C)
        classifier.fit(train_examples, train_labels) # This is the actual training of the classifiers
    
    
    print 'Saving models'
    
    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    f=codecs.open(os.path.join(model_name,u"vectorizer.pkl"),u"wb")
    pickle.dump(vectorizer,f)
    f.close()
    for idx,classifier in enumerate(classifiers):
        f=codecs.open(os.path.join(model_name,u"%d.model.pkl"%idx),u"wb")
        pickle.dump(classifier,f)
        f.close()
    


def test(model_name):
    """ Test all models with the simple F-score, does not use any extra tricks (top nodes allowed per sentence etc...) """
    
    f=codecs.open(os.path.join(model_name,u"vectorizer.pkl"),u"rb")
    vectorizer=pickle.load(f)
    f.close()

    classifiers=[]
    for fname in sorted(glob.glob(os.path.join(model_name,"*.model.pkl"))):
        f=codecs.open(fname,u"rb")
        idx=os.path.basename(fname).split(u".",1)[0]
        classifiers.append((int(idx),pickle.load(f)))
        f.close()

    test_examples=[]
    test_labels=[]

    for comments,sentences,arguments in get_full_sentence(codecs.getreader(u"utf-8")(sys.stdin)):

        if not sentences:
            continue

        for i in xrange(len(sentences[0])): # each sentence has the required information, so we can take just the first one
        
            test_examples.append(create_features(i,sentences[0],arguments))
            test_labels.append(get_label(i,sentences[0]))

    test_examples = vectorizer.transform(test_examples)
    print "Test data has %s examples and %s features" % (test_examples.shape)

    results = []
    for idx,classifier in classifiers:
        f_score = _micro_f_score(test_labels, classifier.predict(test_examples))
        print 'Classifier %s with C value %s achieved F-score %s' % (idx, classifier.C, f_score)
        results.append((classifier, f_score))
        
    results.sort(key=lambda x: x[1], reverse=True) # Sort the classifiers by their F-score
    
    best_classifier, best_f_score = results[0]
    
    print 'Best results with C value %s, F-score %s' % (best_classifier.C, best_f_score)
    
    print classification_report(test_labels, best_classifier.predict(test_examples))
    
   
def _micro_f_score(labels, predictions):
    """
    Calculates F-score. Does this make any sense...?
    """
    
    tp,fp,fn=0.0,0.0,0.0
    
    for i, p in enumerate(predictions):
        if p==1 and p==labels[i]:
            tp+=1
        elif p==1 and p!=labels[i]:
            fp+=1
        elif p==0 and p!=labels[i]:
            fn+=1
        else:
            pass # tn

    # precision
    if tp+fp==0.0:
        pre=0.0
    else:
        pre=tp/(tp+fp)
    # recall
    if (tp+fn)==0.0:
        rec=0.0
    else:
        rec=tp/(tp+fn)
    # F-score
    if pre+rec==0.0:
        return 0.0
    else:
        return 2*pre*rec/(pre+rec)


def filter_predictions(labels,scores,lang):
    """ Filters the predictions using charasteristics of different formats or laguages (eg. can sentence have more than one top node...)
    Rules:
    en.dm, en.pas = exactly one top node per sentence
    en.psd, cs.psd = can have more than one per sentence and each sentence must have a top node
    cz.pas = exactly one top node (Analyzer script shows topless graphs but those are empty sentences...)
    """
    final_top_nodes=[]

    if lang==u"en.dm" or lang==u"en.pas" or lang==u"cz.pas":
        final_top_nodes.append(scores.index(max(scores)))
        return final_top_nodes

    if lang==u"en.psd":
        if labels.count(1)==0:
            final_top_nodes.append(scores.index(max(scores)))
            return final_top_nodes
        for idx,val in enumerate(labels):
            if val==1 and scores[ids] in sorted_scores:
                final_top_nodes.append(idx)
        return final_top_nodes
    if lang==u"cs.psd":
        if labels.count(1)==0:
            final_top_nodes.append(scores.index(max(scores)))
            return final_top_nodes
        sorted_scores=sorted(scores,reverse=True)[:2]
        #print >> sys.stderr,scores
        #print >> sys.stderr,sorted_scores
        for idx,val in enumerate(labels):
            if val==1 and scores[idx] in sorted_scores:
                final_top_nodes.append(idx)
        #print >> sys.stderr, labels.count(1),len(final_top_nodes)
        return final_top_nodes

    assert False
    return final_top_nodes

    
def predict(model_name,lang):

    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)
    out=codecs.getwriter(u"utf-8")(sys.stdout)

    directory=model_name.rsplit(u"/",1)[0]

    f=codecs.open(os.path.join(directory,u"vectorizer.pkl"),u"rb")
    vectorizer=pickle.load(f)
    f.close()

    f=codecs.open(model_name,u"rb")
    classifier=pickle.load(f)
    f.close()

    print >> sys.stderr, "Using model %s with c-value %s" % (model_name,classifier.C)

    for comments,sentences,arguments in get_full_sentence(codecs.getreader(u"utf-8")(sys.stdin)):

        if not sentences:
            print >> out, comments[0]
            print >> out
            continue

        labels=[]
        scores=[]

        for i in xrange(len(sentences[0])): # each sentence has the required information, so we can take just the first one
            
            f=create_features(i,sentences[0],arguments)

            features=vectorizer.transform(create_features(i,sentences[0],arguments))
            label,score=classifier.predict(features)[0],classifier.decision_function(features)[0]
            
            labels.append(label)
            scores.append(score)

        final_top_nodes=filter_predictions(labels,scores,lang) # 0-based token indices

        # print sentences out with top node predictions
        for i in xrange(len(sentences)):
            comment=comments[i]
            sent=sentences[i]
            print >> out, comment
            for idx,line in enumerate(sent):
                if idx in final_top_nodes:
                    line[MISC]=u"TOPNODE=Yes" 
                print >> out, u"\t".join(c for c in line)
            print >> out




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Top node prediction.')
    g=parser.add_argument_group("")
    g.add_argument('--model', required=True, help='Name of the model.')
    g.add_argument('--train', required=False, action="store_true", default=False, help='Train prediction from stdin.')
    g.add_argument('--test', required=False, action="store_true", default=False, help='Test all trained models.')
    g.add_argument('--predict', required=False, action="store_true", default=False, help='Predict top nodes.')
    g.add_argument('--lang', required=False, default=None, help='Language + format (eg. en.dm), needed in prediction')
    args = parser.parse_args()

    if args.train:
        train(args.model)
    elif args.test:
        test(args.model)
    elif args.predict:
        if args.lang is None:
            print >> sys.stderr, "Define --lang when predicting (eg. en.dm)"
            sys.exit(1)
        supported_languages=u"en.dm en.pas en.psd cs.psd cz.pas".split()
        if args.lang not in supported_languages:
            print >> sys.stderr, "Wrong --lang"
            sys.exit(1)
        predict(args.model,args.lang)
    else:
        print >> sys.stderr, "Train, test or predict?"
        sys.exit(1)




