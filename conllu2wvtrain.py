import sys
import codecs
import argparse


def read_conll(f):
    sent=[]
    comment=[]
    for line in f:
        line=line.strip()
        if not line: # new sentence
            if sent:
                yield comment,sent
            comment=[]
            sent=[]
        elif line.startswith(u"#"):
            comment.append(line)
        else: #normal line
            sent.append(line.split(u"\t"))
    else:
        if sent:
            yield comment, sent

def print_sent(sent,args):

    if args.conll09:
        # ID TOKEN LEMMA LEMMA POS POS FEAT FEAT HEAD HEAD DEPREL DEPREL _ _
        POS,FEAT,DEPREL=4,6,10 #conll09
        delim=u"_" # just to make it look prettier...
    else:
        # ID TOKEN LEMMA CPOS POS FEAT HEAD DEPREL DEPS MISC
        POS,FEAT,DEPREL=3,5,7 # conllu
        delim=u"="

    tokens=[]
    for token in sent:
        dtype=u"DTYPE"+delim+token[DEPREL]
        pos=u"POS"+delim+token[POS]
        if args.morpho:
            if args.dtype:
                tokens.append(u"|".join(t for t in [dtype,pos,token[FEAT]] if t!=u"_")) 
            else:
                tokens.append(u"|".join(t for t in [pos,token[FEAT]] if t!=u"_"))           
        elif args.dtype:
            tokens.append(dtype)
        else:
            assert False
    
    print (u" ".join(t for t in tokens)).encode(u"utf-8")

if __name__==u"__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--dtype', default=False, action="store_true", help='Take also deptype.')
    parser.add_argument('--morpho', default=False, action="store_true", help='Take also morpho.')
    parser.add_argument('--conll09', default=False, action="store_true", help='Use conll09 format and not conllu.')
    parser.add_argument('--max_sent', default=15000, type=int, help='Max sent to read.')
    args = parser.parse_args()

    counter=0
    for comment,sent in read_conll(codecs.getreader(u"utf-8")(sys.stdin)):
        counter+=1
        print_sent(sent,args)
        if counter>=args.max_sent:
            break


        
