import sys
import codecs

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
    print >> out, u"\t".join((cols[0],cols[1],cols[2],cols[2],cols[3],cols[3],u"_",u"_",unicode(new_root),unicode(new_root),new_type,new_type))

def gen_one_root(comment,sentence,root_token_idx,predicates):
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
            if types[tok_idx]==u"_":
                one_line(root_token_idx+1,u"NOTARG",cols)
            else:
                one_line(root_token_idx+1,types[tok_idx],cols)
    print >> out
        
def gen(comment,sentence):
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
        gen_one_root(comment,sentence,tok_idx,predicates)
    

if __name__ == "__main__":
    for comment,s in get_sentence(codecs.getreader("utf-8")(sys.stdin)):
        gen(comment,s)

