# -*- coding: utf-8 -*-
from collections import defaultdict

class Tree(object):

    

    def __init__(self,sent,conll=None):
        self.tokens=[]
        self.childs=defaultdict(lambda:set())
        self.deps=[]
        
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
            if gov==0: continue
            gov=lines[gov-1][1]
            dep=line[1]
            dType=line[10]
            self.add_dep(gov,dep,dType)
        self.ready=True

    def add_dep(self,gov,dep,dType):
        self.deps.append((gov,dep,dType))
        self.childs[gov].add(dep)

    def has_dep(self,g,d):
        for dep in self.deps:
            if dep[0]==g.text and dep[1]==d.text:
                return dep[2]
        return None


class Token(object):

    def __init__(self,idx,text,POS=None,feat=None):
        self.index=idx
        self.text=text
        self.POS=POS
        self.feat=feat

    def __str__(self):
        return self.text.encode(u"utf-8")

    def __repr__(self):
        return self.text.encode(u"utf-8")



class Dep(object):

    def __init__(self,gov,dep,dType):
        self.gov=gov
        self.dep=dep
        self.dType=dType
