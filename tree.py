# -*- coding: utf-8 -*-
from collections import defaultdict

class Tree():

    

    def __init__(self,sent,deps=None,conll=None):
        self.tokens=sent.split()
        self.childs=defaultdict(lambda:set())
        self.deps=[]
        
        if conll is not None: # TODO make a function
            for line in conll:
                gov=int(line[8])
                if gov==0: continue
                gov=conll[gov-1][1]
                dep=line[1]
                dType=line[10]
                self.add_dep(gov,dep,dType)
            self.ready=True
        elif deps is not None:
            self.deps=deps
            for dep in deps:
                self.childs[dep[0]].add(dep[1])
            self.ready=True
        else:
            self.deps=[]
            self.ready=False
        

    def add_dep(self,gov,dep,dType):
        self.deps.append((gov,dep,dType))
        self.childs[gov].add(dep)

    def has_dep(self,g,d):
        for dep in self.deps:
            if dep[0]==g and dep[1]==d:
                return dep[2]
        return None


class Token():

    def __init__(self,text,POS,feat):
        self.text=text
        self.POS=POS
        self.feat=feat



class Dep():

    def __init__(self,gov,dep,dType):
        self.gov=gov
        self.dep=dep
        self.dType=dType
