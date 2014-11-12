import sys
import codecs
import argparse
from collections import defaultdict

out=codecs.getwriter("utf-8")(sys.stdout)

def get_sentence(data_in):
    curr_sentence=[]
    curr_comment=None
    for line in data_in:
        
        line=line.strip()
        if not line:
            continue
        if line.startswith(u"#"):
            #New sentence!
            if curr_comment is not None and curr_sentence:
                yield curr_comment, curr_sentence
                curr_comment=None
            curr_comment=line
            curr_sentence=[]
        else: #normal line
            curr_sentence.append(line.split(u"\t"))
    else:
        if curr_comment is not None and curr_sentence:
            yield curr_comment, curr_sentence


def one_line(new_root,new_type,cols):
    global out
    print >> out, u"\t".join((cols[0],cols[1],cols[2],cols[3],u"_",u"_",unicode(new_root),new_type,cols[5]+u":"+cols[6],u"_"))

def gen_one_root(comment,sentence,root_token_idx,predicates,empty):
    global out
    #1) Is this a predicate to begin with?
    print >> out, comment+u".%d"%root_token_idx
    if predicates[root_token_idx] is not None:
        types=[cols[9+predicates[root_token_idx]] for cols in sentence]
    else:
        types=[u"_" for cols in sentence]
    for tok_idx, cols in enumerate(sentence):
        if tok_idx==root_token_idx:
            one_line(0,u"ROOT",cols)
        else:
            if not empty:
                if types[tok_idx]==u"_":
                    one_line(root_token_idx+1,u"NOTARG",cols)
                else:
                    one_line(root_token_idx+1,types[tok_idx],cols)
            else:
                one_line(u"_",u"_",cols)
    print >> out

        
def gen(comment,sentence,empty):
    #Will be generating as many trees as there are tokens in the sentence

    predicates=[] #index of the argument column (0-based) if predicate, None otherwise, as many entries as tokens in the sentence
    counter=0

    if len(sentence[0])<9:
        for cols in sentence:
            cols.append(u"-")
            cols.append(u"-")

    for tok_idx, columns in enumerate(sentence):
        if columns[8]==u"+":
            predicates.append(counter)
            counter+=1
        elif columns[8]==u"-":
            predicates.append(None)
        else:
            assert False
    

    for tok_idx in range(len(sentence)):
        gen_one_root(comment,sentence,tok_idx,predicates,empty)


def build_graph(arguments,idx,sent):
    ''' Use the argument dictionary to build the final graph. '''
    for id,token in enumerate(sent):
        token=token[:6]
        #del token[3] # remove second lemma column
        #del token[4] # remove second pos column
        for i in xrange(2): token.append(u"_")
        for i in xrange(len(arguments)): token.append(u"_")
        sent[id]=token
    pred_count=0
    for pred in sorted(arguments):
        sent[pred-1][5]=u"+"
        pred_count+=1
        args=arguments[pred]
        for arg,argtype in args:
            sent[arg-1][5+pred_count]=argtype
    for i,token in enumerate(sent):
        token[4]=u"-" # root column (TODO)
        if token[5]==u"_":token[5]=u"-" # not predicate
        sent[i]=token     
    print idx
    for t in sent:
        print (u"\t".join(c for c in t)).encode(u"utf-8")
    print

idx=u""
tokens=[]
arguments=defaultdict(lambda:[])
def trees2graph(comment,sent):
    ''' Read trees and collect an argument dictionary. '''
    global arguments,idx,tokens
    gidx,tidx=comment.rsplit(u".",1)
    if gidx!=idx: # this is a new sentence, build the graph from arguments dictionary
        if tokens:
            build_graph(arguments,idx,tokens)
            idx=u""
            tokens=[]
            arguments=defaultdict(lambda:[])
        idx=gidx
    for token in sent:
        if token[7]!=u"NOTARG" and token[7]!=u"ROOT": # this is an argument
            arguments[int(token[6])].append((int(token[0]),token[7]))
        elif token[7]==u"ROOT":
            tokens.append(token)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--empty', default=False, action="store_true", help='Create empty trees (arguments removed, only root dependency included).')
    parser.add_argument('-r', '--reverse', default=False, action="store_true", help='Create a graph from trees.')
    args = parser.parse_args()

    if args.reverse:
        for comment,s in get_sentence(codecs.getreader("utf-8")(sys.stdin)):
            trees2graph(comment,s)
        if tokens: # print last sentence
            build_graph(arguments,idx,tokens)
    else:

        for comment,s in get_sentence(codecs.getreader("utf-8")(sys.stdin)):
            gen(comment,s,args.empty)

