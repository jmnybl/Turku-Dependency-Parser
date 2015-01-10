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


def create_features(sent):
    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

    features=defaultdict(float)

    syntax_heads={}
    syntax_deps={}
    sem_args=[]
    root_id=None
    for line in sent:
        if line[HEAD]==u"0":
            root_id=int(line[ID])-1 # semeval root
        if line[DEPS]!=u"_": # syntax
            syntax_heads[line[ID]]=line[DEPS].split(u":") # head
            # TODO deps
        if line[DEPREL]!=u"_" and line[DEPREL]!=u"ROOT": # semantic argument
            sem_args.append(line[DEPREL])

    features[u"deprel=%s" % syntax_heads[unicode(root_id+1)][1]] = 1.0 # deprel
    features[u"pos=%s" % sent[root_id][POS]] = 1.0 # pos
    features[u"lemma=%s" % sent[root_id][LEMMA]] = 1.0 # lemma
    
    # is predicate
    if sem_args:
        features["predicate=yes"] = 1.0

    # args
    for arg in sem_args:
        features[u"arg=%s" % arg] = 1.0


#    verbId=-1
#    for d in xrange(1,len(sent)):
#        ## dependents
#        gov=sent[d][5]
#        if gov==i: 
#            fSet.add(u"Dep-of-token-"+sent[d][6]+u":1.0")  
#        if sent[d][8]==u"+":
#            verbId+=1
#            if d==i:
#                for j in xrange(1,len(sent)):
#                    # outgoing semantic roles
#                    if sent[j][9+verbId]!=u"_":
#                        fSet.add("role-out-"+sent[j][9+verbId]+u":1.0")
#            if verbId in sem_heads: # search for semantic siblings
#                for j in xrange(1,len(sent)):
#                    if d==j:continue # do not take the current arg
#                    if sent[j][9+verbId]!=u"_":
#                        fSet.add("semantic-sibling-"+sent[j][9+verbId]+u":1.0")
#    # siblings
#    gov=sent[i][5]
#    if gov!=0:
#        for j in xrange(1,len(sent)):
#            if sent[j][5]==gov and j!=i:
#                fSet.add("sibling-"+sent[j][6]+u":1.0")


#    fList=createAllPairs(list(fSet))

    
    return features

def get_label(sent):
    ID,TOKEN,LEMMA,POS,CPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)
    for line in sent:
        if line[HEAD]==u"0" and u"TOPNODE" in line[MISC]:
            return u"1"
    return u"-1"


def train(model_name):
    """
    Trains a classifier to predict top nodes.
    Uses .conllu format, where each sentence is one training example (is root top node?).
    """
    vectorizer = DictVectorizer()
    train_examples=[]
    train_labels=[]
    for comment,sent in get_sentence(codecs.getreader(u"utf-8")(sys.stdin)):
        

        train_examples.append(create_features(sent))
        train_labels.append(get_label(sent))

    pos,neg=0,0
    for label in train_labels:
        if label==u"1":
            pos+=1
        elif label==u"-1":
            neg+=1
        else:
            assert False

    print "Training data has %d positive examples and %d negative examples" % (pos,neg)

    train_examples = vectorizer.fit_transform(train_examples)
    
    print "Training data has %s examples and %s features" % (train_examples.shape)
    
    print "Training classifiers"
    
    c_values = [2**i for i in range(-5, 15)]
    
    classifiers = [LinearSVC(C=c, random_state=1) for c in c_values]
    
    for classifier in classifiers:
        print 'Training classifier with C value %s' % classifier.C
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
    
    f=codecs.open(os.path.join(model_name,u"vectorizer.pkl"),u"rb")
    vectorizer=pickle.load(f)
    f.close()

    classifiers=[]
    for fname in sorted(glob.glob(os.path.join(model_name,"*.model.pkl"))):
        f=codecs.open(fname,u"rb")
        classifiers.append(pickle.load(f))
        f.close()

    test_examples=[]
    test_labels=[]
    for comment,sent in get_sentence(codecs.getreader(u"utf-8")(sys.stdin)):
        
        test_examples.append(create_features(sent))
        test_labels.append(get_label(sent))

    test_examples = vectorizer.transform(test_examples)
    print "Test data has %s examples and %s features" % (test_examples.shape)

    results = []
    for idx,classifier in enumerate(classifiers):
        f_score = _micro_f_score(test_labels, classifier.predict(test_examples))
        print 'Classifier with C value %s achieved F-score %s' % (classifier.C, f_score)
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
        if p=="1" and p==labels[i]:
            tp+=1
        elif p=="1" and p!=labels[i]:
            fp+=1
        elif p==u"-1" and p!=labels[i]:
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
    
def predict(model_name):

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

    for comment,sent in get_sentence(codecs.getreader(u"utf-8")(sys.stdin)):
        
        features=vectorizer.transform(create_features(sent))
        label,score=classifier.predict(features)[0],classifier.decision_function(features)[0]

        if label==u"1":
            for idx,token in enumerate(sent):
                if token[HEAD]==u"0":
                    if token[MISC]==u"_":
                        sent[idx][MISC]=u"TOPNODE=YES"
                    else:
                        sent[idx][MISC]=sent[idx][MISC]+u"|TOPNODE=YES"
                    break
        

        #print label,score
        print >> out, comment
        for token in sent:
            print >> out, u"\t".join(c for c in token)
        print >> out




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Top node prediction.')
    g=parser.add_argument_group("")
    g.add_argument('--model', required=True, help='Name of the model.')
    g.add_argument('--train', required=False, action="store_true", default=False, help='Train prediction from stdin.')
    g.add_argument('--test', required=False, action="store_true", default=False, help='Test all trained models.')
    g.add_argument('--predict', required=False, action="store_true", default=False, help='Predict top nodes.')
    args = parser.parse_args()

    if args.train:
        train(args.model)
    elif args.test:
        test(args.model)
    elif args.predict:
        predict(args.model)
    else:
        print >> sys.stderr, "Train, test or predict?"
        sys.exit(1)




