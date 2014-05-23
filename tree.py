# -*- coding: utf-8 -*-
from collections import defaultdict,namedtuple

CoNLLFormat=namedtuple("CoNLLFormat",["ID","FORM","LEMMA","POS","FEAT","HEAD","DEPREL"])

#Column lists for the various formats
formats={"conll09":CoNLLFormat(0,1,2,4,6,8,10)}

class Tree(object):

    

    def __init__(self,sent,conll=None,syn=False):
        self.tokens=[]
        self.childs=defaultdict(lambda:set())
        self.deps=[]
        self.root=None
        self.projective_order=None
        
        if conll is not None:
            self.from_conll(conll,syn)
        else:
            toks=sent.split()
            for i in xrange(0,len(toks)):
                token=Token(i,toks[i])
                self.tokens.append(token)
            self.deps=[]
            self.ready=False

    def from_conll(self,lines,syn,conll_format="conll09"):    
        """ Reads conll format and transforms it to a tree instance. Form is a format."""
        form=formats[conll_format] #named tuple with the column indices
        for i in xrange(0,len(lines)):
            line=lines[i]
            token=Token(i,line[form.FORM],pos=line[form.POS],feat=line[form.FEAT],lemma=line[form.LEMMA]) # TODO: remove constants :)
            self.tokens.append(token)
        
        if syn:
            for line in lines:
                gov=int(line[form.HEAD])
                if gov==0:
                    self.root=self.tokens[int(line[0])-1]
                    continue
                gov=self.tokens[gov-1]
                dep=self.tokens[int(line[0])-1]
                dType=line[form.DEPREL]
                dependency=Dep(gov,dep,dType)
                self.add_dep(dependency)
            self.ready=True
        else: self.ready=False

    def add_dep(self,dependency):
        self.deps.append(dependency)
        self.childs[dependency.gov].add(dependency.dep)

    def has_dep(self,g,d):
        for dependency in self.deps:
            if dependency.gov.index==g.index and dependency.dep.index==d.index:
                return dependency.dType
        return None


    def is_nonprojective(self):
        """ Return 'non-projective dep' if tree is non-projective, else None"""
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
                    non_projs.add(non_proj)   
        return non_projs

    def define_projective_order(self,tokens):
        # TODO: process set of tokens
        tokens=list(tokens)
        govIdx=None
        main=[]
        sub=[]
        for token in self.tokens:
            if self.part_of_subtree(token,tokens[0]):
                sub.append(token)
            else:
                main.append(token)
            if tokens[0] in self.childs[token]:
                govIdx=token.index
        if govIdx<tokens[0].index: # gov > dep
            self.projective_order=main[:govIdx+1]+sub+main[govIdx+1:]
        else: # dep < gov
            self.projective_order=main[:govIdx]+sub+main[govIdx:]
            
    def part_of_subtree(self,token,subtree_head):
        if token==subtree_head: return True
        if token in self.childs[subtree_head]: return True
        for child in self.childs[subtree_head]:
            return self.part_of_subtree(token,child)
        return False
            

    def is_proj(self,tok1,tok2):
        if (self.tokens.index(tok1)<self.tokens.index(tok2)) and (self.projective_order.index(tok1)>self.projective_order.index(tok2)): return True
        elif (self.tokens.index(tok1)>self.tokens.index(tok2)) and (self.projective_order.index(tok1)<self.projective_order.index(tok2)): return True
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


