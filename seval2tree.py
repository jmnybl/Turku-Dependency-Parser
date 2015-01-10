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
        if not line or line==u"#SDP 2015":
            continue
        if line.startswith(u"#"):
            #New sentence!
            if curr_comment is not None:
                yield curr_comment, curr_sentence
                curr_comment=None
            curr_comment=line
            curr_sentence=[]
        else: #normal line
            curr_sentence.append(line.split(u"\t"))
    else:
        if curr_comment is not None and curr_sentence:
            yield curr_comment, curr_sentence

def read_companion(data_in):
    """ Do not rely # lines to be comments. """
    curr_sentence=[]
    curr_comment=None
    for line in data_in:
        line=line.strip()
        if line==u"#SDP 2015":
            continue
        if not line:
            yield curr_comment, curr_sentence
            curr_comment=None
            curr_sentence=[]
        elif line.startswith(u"#") and (curr_comment is None):
            curr_comment=line
        else: #normal line
            curr_sentence.append(line.split(u"\t"))
    else:
        if curr_comment is not None and curr_sentence:
            yield curr_comment, curr_sentence


#def one_line(new_root,new_type,cols,deps_field,format):
#    global out
#    ID,TOKEN,LEMMA,POS,TOP,PRED,SENSE,ARGS=range(8)
#    # conllu format:
#    # ID TOKEN LEMMA POS UPOS FEAT HEAD DEPREL DEPS MISC
#    if format==u"2015":
#        print >> out, u"\t".join((cols[ID],cols[TOKEN],cols[LEMMA],cols[POS],u"_",u"_",unicode(new_root),new_type,deps_field,cols[SENSE]))
#    else: # no sense
#        print >> out, u"\t".join((cols[ID],cols[TOKEN],cols[LEMMA],cols[POS],u"_",u"_",unicode(new_root),new_type,deps_field,u"_"))



def analyze_morpho(m):
    CATS=u"Gen, Num, Cas, PGe, PNu, Per, Ten, Gra, Neg, Voi, Var".split(u", ") #From Dan's email
    CPOS=m[0]
    POS=m[:2]
    assert u"-" not in POS
    feat=[]
    for CAT,VAL in zip(CATS,m[2:13]):
        if VAL!=u'-':
            feat.append(CAT+u"="+VAL)
    if feat:
        feat_str=u"|".join(feat)
    else:
        feat_str=u"_"
    return CPOS,POS,feat_str

def gen_one_root(comment,sentence,root_token_idx,predicates,empty,comp,format):
    global out

    if format==u"2015":
        ID,TOKEN,LEMMA,POS,TOP,PRED,SENSE,ARGS=range(8)
    else:
        ID,TOKEN,LEMMA,POS,TOP,PRED,ARGS=range(7)

    print >> out, comment+u".%d"%root_token_idx
    #1) Is this a predicate to begin with?
    if predicates[root_token_idx] is not None:
        types=[cols[ARGS+predicates[root_token_idx]] for cols in sentence]
    else:
        types=[u"_" for cols in sentence]
    for tok_idx, cols in enumerate(sentence):
        DEPS=comp.get(tok_idx,u"_")
        if format==u"2015" and not empty: # include senses or not?
            if cols[SENSE]!=u"_" or cols[TOP]==u"+":
                sense=u"SENSE="+cols[SENSE] if cols[SENSE]!=u"_" else None
                top=u"TOPNODE=Yes" if cols[TOP]==u"+" else None
                MISC=u"|".join(i for i in [sense,top] if i is not None)
            else:
                MISC=u"_"
        else:
            MISC=u"_"
        if len(cols[POS])==15: # split czech POS tags
            pos,cpos,feats=analyze_morpho(cols[POS])
        else:
            pos=cols[POS]
            cpos=u"_"
            feats=u"_"
        if tok_idx==root_token_idx:
            #one_line(0,u"ROOT",cols,deps_field)
            print >> out, u"\t".join((cols[ID],cols[TOKEN],cols[LEMMA],pos,cpos,feats,u"0",u"ROOT",DEPS,MISC))
        else:
            if not empty:
                if types[tok_idx]==u"_":
                    #one_line(root_token_idx+1,u"NOTARG",cols,deps_field,format)
                    print >> out, u"\t".join((cols[ID],cols[TOKEN],cols[LEMMA],pos,cpos,feats,unicode(root_token_idx+1),u"NOTARG",DEPS,MISC))
                else:
                    #one_line(root_token_idx+1,types[tok_idx],cols,deps_field,format)
                    print >> out, u"\t".join((cols[ID],cols[TOKEN],cols[LEMMA],pos,cpos,feats,unicode(root_token_idx+1),types[tok_idx],DEPS,MISC))
            else:
                #one_line(u"_",u"_",cols,deps_field,format)
                print >> out, u"\t".join((cols[ID],cols[TOKEN],cols[LEMMA],pos,cpos,feats,u"_",u"_",DEPS,MISC))
    print >> out

        
def gen(comment,sentence,empty,comp,format):
    #Will be generating as many trees as there are tokens in the sentence
    # empty: create empty trees (for testing)
    # comp: companion data (syntactic parses) to be included as extra structure (dictionary, key: 0-based id, value: "head:deprel")

    ID,TOKEN,LEMMA,POS,TOP,PRED,SENSE,ARGS=range(8)

    predicates=[] #index of the argument column (0-based) if predicate, None otherwise, as many entries as tokens in the sentence
    counter=0

    if not empty:
        for tok_idx, columns in enumerate(sentence):
            if columns[PRED]==u"+":
                predicates.append(counter)
                counter+=1
            elif columns[PRED]==u"-":
                predicates.append(None)
            else:
                assert False
    else:
        for i in range(len(sentence)):
            predicates.append(None)
    

    for tok_idx in range(len(sentence)):
        gen_one_root(comment,sentence,tok_idx,predicates,empty,comp,format)


def build_graph(arguments,idx,sent,format):
    ''' Use the argument dictionary to build the final graph. '''
    if format==u"2015":
        ID,TOKEN,LEMMA,POS,TOP,PRED,SENSE,ARGS=range(8)
    else:
        ID,TOKEN,LEMMA,POS,TOP,PRED,ARGS=range(7)

    HEAD,DEPREL,DEPS,MISC=6,7,8,9

    for id,token in enumerate(sent):
        cols=token[:4]
        for i in xrange(2): cols.append(u"_") # TOP and PRED empty
        if format==u"2015":
            cols.append(token[MISC]) # sense from MISC field
        for i in xrange(len(arguments)): cols.append(u"_") # append empty places for arguments
        sent[id]=cols
    pred_count=0
    for pred in sorted(arguments):
        sent[pred-1][PRED]=u"+" # PRED == +
        pred_count+=1
        args=arguments[pred]
        for arg,argtype in args:
            sent[arg-1][ARGS-1+pred_count]=argtype
    for i,token in enumerate(sent):
        token[TOP]=u"-" # top node (TODO)
        if token[PRED]==u"_": token[PRED]=u"-" # not predicate
        sent[i]=token     
    print idx
    for t in sent:
        print (u"\t".join(c for c in t)).encode(u"utf-8")
    print

idx=u""
tokens=[]
arguments=defaultdict(lambda:[])
def trees2graph(comment,sent,format):
    ''' Read trees and collect an argument dictionary. '''

    ID,TOKEN,LEMMA,POS,UPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

    global arguments,idx,tokens
    gidx,tidx=comment.rsplit(u".",1)
    if gidx!=idx: # this is a new sentence, build the graph from arguments dictionary
        if tokens:
            build_graph(arguments,idx,tokens,format)
            idx=u""
            tokens=[]
            arguments=defaultdict(lambda:[])
        idx=gidx
    for token in sent:
        if token[DEPREL]!=u"NOTARG" and token[DEPREL]!=u"ROOT": # this is an argument
            arguments[int(token[HEAD])].append((int(token[ID]),token[DEPREL]))
        elif token[HEAD]==u"0":
            tokens.append(token)

if __name__ == "__main__":
    
    # semantic graphs data:
    # 1  2     3     4   5   6    7     8+
    # ID TOKEN LEMMA POS TOP PRED SENSE ARGS+

    # companion data
    # 1   2    3
    # POS HEAD DEPREL

    parser = argparse.ArgumentParser()
    parser.add_argument('--companion', default=None, help='Companion data.')
    parser.add_argument('--empty', default=False, action="store_true", help='Create empty trees (arguments removed, only root dependency included).')
    parser.add_argument('-r', '--reverse', default=False, action="store_true", help='Create a graph from trees.')
    parser.add_argument('--format', default="2015", help='Data format, 2014 or 2015 (do we have senses or not)')
    args = parser.parse_args()

    if args.reverse: # build sdp graphs from conllu trees
        if args.format==u"2015": # 2015 Scorer requires this line
            print >> out, u"#SDP 2015"
        for comment,s in get_sentence(codecs.getreader("utf-8")(sys.stdin)):
            if not s: # empty sentence
                print >> out, comment
                print >> out
                continue
            trees2graph(comment,s,args.format)
        if tokens: # print last sentence
            build_graph(arguments,idx,tokens,args.format)

    else: # build conllu trees from sdp graphs
        if args.companion is None:
            for comment,s in get_sentence(codecs.getreader("utf-8")(sys.stdin)):
                if not s: # empty sentence
                    print >> out, comment
                    print >> out
                    continue
                gen(comment,s,args.empty,{},args.format)
        else: # use companion data
            syntax={}
            with codecs.open(args.companion, u"rt", u"utf-8") as f:
                for comm,s in read_companion(f):
                    syntax[comm]=s
            for comment,s in get_sentence(codecs.getreader("utf-8")(sys.stdin)):
                if not s: # empty sentence
                    print >> out, comment
                    print >> out
                    continue
                assert comment in syntax, "No companion data found: "+comment
                comp={}
                for idx,line in enumerate(syntax[comment]):
                    # TODO: do we ever want to use this POS?
                    comp[idx]=u":".join([line[1],line[2]])
                gen(comment,s,args.empty,comp,args.format)








