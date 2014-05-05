# -*- coding: utf-8 -*-


class Tree():

    def __init__(self):
        self.deps=[]
        self.ready=False

    def add_dep(self,gov,dep,dType):
        self.deps.append((gov,dep,dType))


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
