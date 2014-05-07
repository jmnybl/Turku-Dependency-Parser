# -*- coding: utf-8 -*-
import collections

class Tree():

    

    def __init__(self,sent,deps=None):
        self.tokens=sent.split()
        self.childs=collections.defaultdict(lambda:set())
        if deps is None:
            self.deps=[]
            self.ready=False
        else:
            self.deps=deps
            for dep in deps:
                self.childs[dep[0]].add(dep[1])
            self.ready=True

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
