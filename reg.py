from conllu2wvtrain import read_conll
from wvlib import wvlib
import codecs
import sys
import argparse
import regressor
import numpy


def process_sent(sent,args):
    # ID TOKEN LEMMA LEMMA POS POS FEAT FEAT HEAD HEAD DEPREL DEPREL _ _
    if args.conll09:
        # ID TOKEN LEMMA LEMMA POS POS FEAT FEAT HEAD HEAD DEPREL DEPREL _ _
        POS,FEAT,DEPREL=4,6,10 #conll09
        TOKEN,POS,FEAT,HEAD,DEPREL=1,4,6,8,10 #conll09
        delim=u"_" # just to make it look prettier...
    else:
        # ID TOKEN LEMMA CPOS POS FEAT HEAD DEPREL DEPS MISC
        TOKEN,POS,FEAT,HEAD,DEPREL=1,3,5,6,7 # conllu
        delim=u"="
    
    tokens=[]
    for token in sent:
        if token[HEAD]==u"0":
            continue # skip root tokens
        dtoken=token[TOKEN]
        dpos=u"POS"+delim+token[POS]        
        gtoken=sent[int(token[HEAD])-1][TOKEN]
        gpos=u"POS"+delim+sent[int(token[HEAD])-1][POS]
        ddtype=u"DTYPE"+delim+token[DEPREL]
        gdtype=u"DTYPE"+delim+sent[int(token[HEAD])-1][DEPREL]
        if args.morpho:
            if args.dtype:
                dvalue=u"|".join(t for t in [ddtype,dpos,token[FEAT]] if t!=u"_")
                gvalue=u"|".join(t for t in [gdtype,gpos,sent[int(token[HEAD])-1][FEAT]] if t!=u"_")
            else:
                dvalue=u"|".join(t for t in [dpos,token[FEAT]] if t!=u"_")
                gvalue=u"|".join(t for t in [gpos,sent[int(token[HEAD])-1][FEAT]] if t!=u"_")
        elif args.dtype:
            dvalue=ddtype
            gvalue=gdtype

        tokens.append((dtoken,gtoken,dvalue,gvalue))
    return tokens

def tokens2vector((dtok,gtok),tmodel):
    try:
        dvec=tmodel.word_to_vector(dtok)
        gvec=tmodel.word_to_vector(gtok)
        return dvec,gvec
    except:
        #print >> sys.stderr, "vectors not found:", dtok,gtok
        return None,None


def train(args,vr,lr):

    tmodel=wvlib.load(args.wvtoken, max_rank=10000).normalize()
    mmodel=wvlib.load(args.wvmorpho, max_rank=10000).normalize()

    f=codecs.open(u"tdt-train-jktagged.conll09",u"rt",u"utf-8")
    #f=codecs.open(u"/usr/share/ParseBank/DepLing2015/fi-tdt-train.conllu",u"rt",u"utf-8")
    for comment,sent in read_conll(f):#(codecs.getreader(u"utf-8")(sys.stdin)):
        examples=process_sent(sent,args)
        for example in examples:
            dvec,gvec=tokens2vector(example[:2],tmodel)
            try:
                mvec=mmodel.word_to_vector(example[2])
                govmorpho=mmodel.word_to_vector(example[3])
            except:
                mvec=None
                govmorpho=None
            if (dvec is not None) and (gvec is not None) and (mvec is not None) and (govmorpho is not None):
                #print repr(dvec),repr(gvec)
                #print numpy.concatenate(dvec,gvec)
                #print vr.update(numpy.concatenate((dvec,gvec,govmorpho)),mvec,lr)
                print vr.update(numpy.concatenate((dvec,gvec)),mvec,lr)

def predict(args,vr):
    total=0
    correct=0
    tmodel=wvlib.load(args.wvtoken, max_rank=10000).normalize()
    mmodel=wvlib.load(args.wvmorpho, max_rank=10000).normalize()
    #f=codecs.open(u"/usr/share/ParseBank/tdt_test.conll09",u"rt",u"utf-8")
    f=codecs.open(u"/usr/share/ParseBank/DepLing2015/fi-tdt-fulldev.conllu",u"rt",u"utf-8")
    for comment,sent in read_conll(f): #read_conll(codecs.getreader(u"utf-8")(sys.stdin)):
        examples=process_sent(sent,args)
        for example in examples:
            dvec,gvec=tokens2vector(example[:2],tmodel)
            try:
                gmorpho=mmodel.word_to_vector(example[3])
                gs=mmodel.word_to_vector(example[2])
            except:
                gmorpho=None
                gs=None
            if (dvec is not None) and (gvec is not None) and (gmorpho is not None) and (gs is not None):
                total+=1
                #mvec=vr.predict(numpy.concatenate((dvec,gvec,gmorpho)))
                mvec=vr.predict(numpy.concatenate((dvec,gvec)))
                predicted=mmodel.nearest(mvec.astype(numpy.float32))[0]
                if example[2]==predicted[0]:
                    correct+=1
                print example[0],example[2],predicted,mmodel.similarity(gs,predicted[0])
    print "%d/%d"%(correct,total)
    


if __name__==u"__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--wvtoken', default=u"/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin", help='Word2vec model for tokens.')
    parser.add_argument('--wvmorpho', default=u"vectors.morpho.pb.bin", help='Word2vec model for morpho vectors.')
    parser.add_argument('--dtype', default=False, action="store_true", help='Take also deptype.')
    parser.add_argument('--morpho', default=False, action="store_true", help='Take also morpho.')
    parser.add_argument('--conll09', default=False, action="store_true", help='Use conll09 format and not conllu.')
    args = parser.parse_args()

    vr=regressor.VRegressor(600,10)

    lr=0.01
    for i in range(5):
        train(args,vr,lr)
        lr=0.75*lr
    predict(args,vr)
