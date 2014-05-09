# -*- coding: utf-8 -*-
from collections import defaultdict

class Tree(object):

    

    def __init__(self,sent,conll=None):
        self.tokens=[]
        self.childs=defaultdict(lambda:set())
        self.deps=[]
        self.root=None
        self.projective_order=None
        
        if conll is not None:
            self.from_conll(conll)
        else:
            toks=sent.split()
            for i in xrange(0,len(toks)):
                token=Token(i,toks[i])
                self.tokens.append(token)
            self.deps=[]
            self.ready=False

    def from_conll(self,lines):    
        """ Reads conll format and transforms it to a tree instance. """
        for i in xrange(0,len(lines)):
            line=lines[i]
            token=Token(i,line[1])
            self.tokens.append(token)
        for line in lines:
            gov=int(line[8])
            if gov==0:
                self.root=self.tokens[int(line[0])-1]
                continue
            gov=self.tokens[gov-1]
            dep=self.tokens[int(line[0])-1]
            dType=line[10]
            dependency=Dep(gov,dep,dType)
            self.add_dep(dependency)
        self.ready=True

    def add_dep(self,dependency):
        self.deps.append(dependency)
        self.childs[dependency.gov].add(dependency.dep)

    def has_dep(self,g,d):
        for dependency in self.deps:
            if dependency.gov.index==g.index and dependency.dep.index==d.index:
                return dependency.dType
        return None

    def is_nonprojective(self):
        rootdep=Dep(Token(-1,u""),self.root,u"dummydep")
        for i in xrange(0,len(self.deps)):
            dep1=self.deps[i]
            for j in xrange(i+1,len(self.deps)):
                dep2=self.deps[j]
                if dep1.gov==dep2.gov or dep1.dep==dep2.dep or dep1.gov==dep2.dep or dep1.dep==dep2.gov: continue
                if dep1.is_crossing(dep2): return True
            if dep1.is_crossing(rootdep): return True
        return False

    def define_projective_order(self,subtree):
        main=[]
        sub=[]
        for token in self.tokens:
            if self.part_of_subtree(token,subtree):
                sub.append(token)
            else:
                main.append(token)
        if True: #TODO: where to attach?
            self.projective_order=main+subtree
        else: self.projective_order=subtree+main
            
    def part_of_subtree(self,token,subtree):
        pass # TODO
            


class Token(object):

    def __init__(self,idx,text,POS=None,feat=None):
        self.index=idx
        self.text=text
        self.POS=POS
        self.feat=feat

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
        if self.gov.index<another.gov.index<self.dep.index:
            if self.gov.index<another.dep.index<self.dep.index:
                return False
            else: return True
        elif self.gov.index>another.gov.index>self.dep.index:
            if self.gov.index>another.dep.index>self.dep.index:
                return False
            else: return True
        elif self.gov.index<another.dep.index<self.dep.index:
            if self.gov.index<another.gov.index<self.dep.index:
                return False
            else: return True
        elif self.gov.index>another.dep.index>self.dep.index:
            if self.gov.index>another.gov.index>self.dep.index:
                return False
            else: return True
        return False

    def __str__(self):
        return (u"<Gov:"+unicode(self.gov.index)+u",Dep:"+unicode(self.dep.index)+u",dType:"+self.dType+u">").encode(u"utf-8")

    def __repr__(self):
        return (u"<Gov:"+unicode(self.gov.index)+u",Dep:"+unicode(self.dep.index)+u",dType:"+self.dType+u">").encode(u"utf-8")


