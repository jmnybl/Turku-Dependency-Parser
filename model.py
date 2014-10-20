import sys
import os
import cPickle
import codecs
from collections import defaultdict
from tree import formats,read_conll

class Model(object):

    """ This object stores external information (like corpus statistics etc.) """

    @classmethod
    def load(cls,model_name):
        f=codecs.open(model_name,u"rb")
        data=cPickle.load(f)
        f.close()
        model=cls(data)
        return model

    @classmethod
    def collect(cls,model_name,corpus,cutoff=2,conll_format="conll09"):
        form=formats[conll_format]
        pairs=defaultdict(lambda:0)
        for sent,comment in read_conll(corpus):
            for token in sent:
                gov=int(token[form.HEAD])
                if gov==0: continue # ROOT
                gov_pos=sent[gov-1][form.POS]
                pos,deprel=token[form.POS],token[form.DEPREL]
                pairs[(gov_pos,pos,deprel)]+=1
        types={}
        for (gov_pos,pos,deprel),value in pairs.iteritems():
            if value>cutoff:
                types.setdefault((gov_pos,pos),set()).add(deprel)
        # now we have collected the dictionary, pickle it and create a model instance
        f=codecs.open(model_name,u"wb")
        cPickle.dump(types,f)
        f.close()
        model=cls(types)
        return model
        


    def __init__(self,model):
        if model is None:
            raise ValueError("Create model object by calling load() or collect()")            
        self.deptypes=model # {key:(gov_pos,dep_pos), value:set of possible deptypes} dictionary



if __name__==u"__main__":

    # simple test
    model_name=u"corpus_stats.pkl"
    if os.path.exists(model_name):
        print >> sys.stderr, "loading file:",model_name
        model=Model.load(model_name)
    else:
        print >> sys.stderr, "collecting stats from tdt.conll"
        model=Model.collect(model_name,"tdt.conll")
    print model.deptypes
    
    
