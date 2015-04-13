# -*- coding: utf-8 -*-
from collections import defaultdict,namedtuple
import codecs
import copy

CoNLLFormat=namedtuple("CoNLLFormat",["ID","FORM","LEMMA","POS","FEAT","HEAD","DEPREL"])

#conllu
#0  1    2     3    4   5    6     7     8    9
#ID FORM LEMMA CPOS POS FEAT HEAD DEPREL DEPS MISC

#Column lists for the various formats
formats={"conll09":CoNLLFormat(0,1,2,4,6,8,10),"conllu":CoNLLFormat(0,1,2,4,5,6,7)}



def read_conll(inp):
    """ Read conll format file and yield one sentence at a time as a list of lists of columns. If inp is a string it will be interpreted as filename, otherwise as open file for reading in unicode"""
    if isinstance(inp,basestring):
        f=codecs.open(inp,u"rt",u"utf-8")
    else:
        f=inp

    sent=[]
    for line in f:
        line=line.strip()
        if not line or line.startswith(u"#"): #Do not rely on empty lines in conll files, ignore comments
            continue 
        if line.startswith(u"1\t") and sent: #New sentence, and I have an old one to yield
            yield sent
            sent=[]
        sent.append(line.split(u"\t"))
    else:
        if sent:
            yield sent

    if isinstance(inp,basestring):
        f.close() #Close it if you opened it

def fill_conll(sent,state,conll_format=u"conllu"):
    form=formats[conll_format]
    for i in xrange(0,len(sent)):
        token=state.tree.tokens[i]
#        if token not in state.tree.govs: # ROOT
#            sent[i][form.HEAD]=u"0"
#            sent[i][form.DEPREL]=u"ROOT"
#        else:
        sent[i][form.HEAD]=unicode(state.tree.govs[token].index+1)
        if state.tree.govs[token].index+1==0: # hard-code deprel to be ROOT
            sent[i][form.DEPREL]=u"ROOT"
        else:
            sent[i][form.DEPREL]=state.tree.dtypes[token]

def write_conll(f,sent):
    for line in sent:
        f.write(u"\t".join(c for c in line)+u"\n")
    f.write(u"\n")

class Tree(object):

    @classmethod
    def new_from_conll(cls,conll,syn,conll_format="conllu"):
        t=cls()
        t.from_conll(conll,syn,conll_format)
        return t

    @classmethod
    def new_from_tree(cls,t):
        """Selectively copies only those parts that can change during parse"""
        newT=cls.__new__(cls) #Do not call the __init__() because we will fill the args by hand
        newT.tokens=t.tokens
        newT.childs=defaultdict(lambda:set())
        for tok,s in t.childs.iteritems():
            if tok in t.ready_nodes:
                newT.childs[tok]=s # this one is ready, no need to copy
            else:
                newT.childs[tok]=s.copy()
        newT.ready_nodes=t.ready_nodes.copy() # this needs to be copied
        newT.govs=t.govs.copy()
        newT.deps=t.deps[:]
        newT.dtypes=t.dtypes.copy()
        newT.root=t.root
        newT.projective_order=t.projective_order #no need to copy this one
        newT.ready=t.ready
        return newT

    def __init__(self):
        #If you add any new attributes, make sure you copy them over in new_from_tree()
        self.tokens=[] #[Token(),...]
        self.childs=defaultdict(lambda:set()) #{token():set(token())#
        self.ready_nodes=set() # set(token())
        self.govs={} #{token():govtoken()}
        self.dtypes={} #{token():dtype}
        self.deps=[] #[Dep(),...]
        self.root=None #?
        self.projective_order=None 
        self.ready=False

    #Called from new_from_conll() classmethod
    def from_conll(self,lines,syn,conll_format="conll09"):    
        """ Reads conll format and transforms it to a tree instance. `conll_format` is a format name
            which will be looked up in the formats module-level dictionary"""
        form=formats[conll_format] #named tuple with the column indices
        for i in xrange(0,len(lines)): # create tokens
            line=lines[i]
            token=Token(i,line[form.FORM],pos=line[form.POS],feat=line[form.FEAT],lemma=line[form.LEMMA])
            self.tokens.append(token)

        
        if syn: # create dependencies
            for line in lines:
                self.dtypes[self.tokens[int(line[form.ID])-1]]=line[form.DEPREL] # fill dtype for token
                gov=int(line[form.HEAD])
                if gov==0:
                    self.root=self.tokens[int(line[0])-1] # TODO: why I store this information?
                    continue
                gov=self.tokens[gov-1]
                dep=self.tokens[int(line[0])-1]
                dType=line[form.DEPREL]
                dependency=Dep(gov,dep,dType)
                self.add_dep(dependency)
            self.ready=True
            self.ready_nodes=set(self.tokens) # all nodes are ready
        else: 
            self.ready=False

    def add_dep(self,dependency):
        self.deps.append(dependency)
        self.childs[dependency.gov].add(dependency.dep)
        self.govs[dependency.dep]=dependency.gov
        self.dtypes[dependency.dep]=dependency.dType
        self.ready_nodes.add(dependency.dep)

    def has_dep(self,g,d):
        for dependency in self.deps:
            if dependency.gov.index==g.index and dependency.dep.index==d.index:
                return dependency.dType
        return None


    def is_nonprojective(self):
        """ Return 'non-projective tokens' if tree is non-projective, else empty set"""
        non_projs=set()
        rootdep=Dep(Token(-1,u""),self.root,u"dummydep")
        for i in xrange(0,len(self.deps)):
            dep1=self.deps[i]
            if dep1.gov!=self.root and dep1.dep!=self.root:
                non_proj=dep1.is_crossing(rootdep)
                if non_proj is not None:
                    non_projs.add(dep1.dep)
            for j in xrange(i+1,len(self.deps)):
                dep2=self.deps[j]
                if dep1.gov==dep2.gov or dep1.dep==dep2.dep or dep1.gov==dep2.dep or dep1.dep==dep2.gov: continue
                non_proj=dep1.is_crossing(dep2)
                if non_proj is not None:
                    if self.part_of_subtree(dep1.dep,dep2.gov): 
                        non_projs.add(dep1.dep)
                    elif self.part_of_subtree(dep2.dep,dep1.gov):
                        non_projs.add(dep2.dep)
                    elif dep1.dep.index<dep2.dep.index:
                        non_projs.add(dep1.dep)
                    else:
                        non_projs.add(dep2.dep) 
        return non_projs

    def define_projective_order(self,tokens):
        tokens=list(tokens)
        order=self.tokens[:]
        while tokens:
            govIdx=None
            main=[]
            sub=[]
            idx=0
            for token in order:
                if self.part_of_subtree(token,tokens[0]):
                    sub.append(token)
                else:
                    main.append(token)
                if tokens[0] in self.childs[token]:
                    govIdx=idx
                idx+=1
            if govIdx<tokens[0].index: # gov > dep
                order=main[:govIdx+1]+sub+main[govIdx+1:]
            else: # dep < gov
                order=main[:govIdx-1]+sub+main[govIdx-1:]
            t=tokens.pop(0)
        self.projective_order=order
            
    def part_of_subtree(self,token,subtree_head):
        if token==subtree_head: return True
        if token in self.childs[subtree_head]: return True
        for child in self.childs[subtree_head]:
            if self.part_of_subtree(token,child):
                return True
        return False
            

    def is_proj(self,tok1,tok2):
        if tok1.index==-1 or tok2.index==-1: # artificial root token, not part of the self.projective order
            return False # TODO: do I ever want to SWAP root?
        if (tok1.index<tok2.index) and (self.projective_order.index(tok1)>self.projective_order.index(tok2)): return True
        elif (tok1.index>tok2.index) and (self.projective_order.index(tok1)<self.projective_order.index(tok2)): return True
        else: return False



class Token(object):

    def __init__(self,idx,text,pos="",feat="",lemma=""):
        self.index=idx
        self.text=text
        self.pos=pos
        self.feat=feat
        self.lemma=lemma

    def __str__(self):
        return self.text.encode(u"utf-8")

    def __repr__(self):
        return (u"<"+self.text+u">").encode(u"utf-8")

    def __eq__(self,other):
        return self.index==other.index

    def __hash__(self):
        return hash(self.index)



class Dep(object):

    def __init__(self,gov,dep,dType):
        self.gov=gov
        self.dep=dep
        self.dType=dType

    def is_crossing(self,another):
        if self.is_between(self.gov.index,self.dep.index,another.dep.index)==True and self.is_between(self.gov.index,self.dep.index,another.gov.index)==False:
            return another.dep
        elif self.is_between(another.gov.index,another.dep.index,self.dep.index)==True and self.is_between(another.gov.index,another.dep.index,self.gov.index)==False:
            return self.dep
        else:
            return None


    def is_between(self,i1,i2,target):
        if (i1<target<i2) or (i2<target<i1):
            return True
        else: return False


    def __str__(self):
        return (u"<Gov:"+unicode(self.gov.index)+u",Dep:"+unicode(self.dep.index)+u",dType:"+self.dType+u">").encode(u"utf-8")

    def __repr__(self):
        return (u"<Gov:"+unicode(self.gov.index)+u",Dep:"+unicode(self.dep.index)+u",dType:"+self.dType+u">").encode(u"utf-8")


