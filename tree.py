# -*- coding: utf-8 -*-
from collections import defaultdict,namedtuple
import codecs
import copy
import itertools

CoNLLFormat=namedtuple("CoNLLFormat",["ID","FORM","LEMMA","POS","FEAT","HEAD","DEPREL","EXTRA"])

#Column lists for the various formats
formats={"conll09":CoNLLFormat(0,1,2,4,6,8,10,12),"conll-u":CoNLLFormat(0,1,2,3,5,6,7,8)}



def read_conll(inp):
    """ Read conll format file and yield one sentence at a time as a list of lists of columns. If inp is a string it will be interpreted as filename, otherwise as open file for reading in unicode"""
    if isinstance(inp,basestring):
        f=codecs.open(inp,u"rt",u"utf-8")
    else:
        f=inp

    sent=[]
    comments=[]
    for line in f:
        line=line.strip()
        if not line:
            if sent:
                yield sent, comments
            sent=[]
            comments=[]
        elif line.startswith(u"#"):
            if sent:
                raise ValueError("Missing newline after sentence")
            comments.append(line)
            continue
        else:
            sent.append(line.split(u"\t"))
    else:
        if sent:
            yield sent, comments

    if isinstance(inp,basestring):
        f.close() #Close it if you opened it


def fill_conll(sent,state,conll_format=u"conll-u"):
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
def write_conll(f,sent,comments=[]):
    for comm in comments:
        f.write(comm+u"\n")
    for line in sent:
        f.write(u"\t".join(c for c in line)+u"\n")
    f.write(u"\n")

class Tree(object):

    @classmethod
    def new_from_conll(cls,conll,conll_format="conll-u",extra_tree=True): # TODO extra_tree
        t=cls()
        form=formats[conll_format]
        if conll[0][form.EXTRA]!=u"_" and extra_tree: # if not empty TODO
            extra=Tree() # create empty tree
        else:
            extra=None
        t.from_conll(conll,conll_format,extra)
        return t,extra

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
        self.semeval_root_idx=None
        self.context={}
        self.route={}

    def BFS_queue(self,token):
        result_dict={token:0} #itself at distance 0
        self.BFS_order(token,0,result_dict) 
        #result_dict should now have a distance for every reachable token
        #dependency distance from token, linear distance from token, position in sentence, and the second token itself
        queue=[(dis,abs(t.index-token.index),t.index,t) for t,dis in result_dict.iteritems()]
        queue.sort()
        return [item[-1] for item in queue] #pick just the token, nothing else

    def BFS_order(self,token,distance,result_dict):
        """
        result_dict {token:distance}
        """
        for t in itertools.chain(self.childs[token],[self.govs.get(token,None)]):
            if t is not None and t not in result_dict: #not visited yet (can happen on the way up in the tree) and not None (could come from .govs)
                result_dict[t]=distance+1 #children and roots are at a distance one longer than the token itself
                self.BFS_order(t,distance+1,result_dict)

    #Called from new_from_conll() classmethod
    def from_conll(self,lines,conll_format="conll-u",extra=None):
        """ Reads conll format and transforms it to a tree instance. `conll_format` is a format name
            which will be looked up in the formats module-level dictionary"""
        form=formats[conll_format] #named tuple with the column indices
        for i in xrange(0,len(lines)): # create tokens
            line=lines[i]
            token=Token(i,line[form.FORM],pos=line[form.POS],feat=line[form.FEAT],lemma=line[form.LEMMA])
            self.tokens.append(token)
            if extra is not None:
                extra.tokens.append(token)
            if line[form.DEPREL]==u"ROOT":
                self.semeval_root_idx=i
                self.tokens[-1].is_semeval_root=True
            else:
                self.tokens[-1].is_semeval_root=False
        self.ready=False
        if extra is not None: # create extra tree
            for line in lines:
                head,deprel=line[form.EXTRA].split(u":")
                extra.dtypes[extra.tokens[int(line[form.ID])-1]]=deprel # fill dtype for token
                gov=int(head)
                if gov==0:
                    extra.root=extra.tokens[int(line[form.ID])-1] # TODO: why I store this information?
                    continue
                gov=extra.tokens[gov-1]
                dep=extra.tokens[int(line[form.ID])-1]
                dependency=Dep(gov,dep,deprel)
                extra.add_dep(dependency)
            extra.ready=True
            extra.ready_nodes=set(self.tokens) # all nodes are ready

    def fill_syntax(self,sent,conll_format="conll-u"):
        form=formats[conll_format] #named tuple with the column indices
        for line in sent:
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

    def __str__(self):
        return (u",".join(str(d) for d in self.deps)).encode(u"utf-8")


    def get_token_tree_context(self, token, max_len=3, route=[]):

        #If max_len less than 1 return what was given
        if max_len < 1:
            return [route]

        #Get every dep in which current token is mentioned
        where_to_go = []
        for dep in self.deps:
            if token == dep.gov and dep not in route:
                where_to_go.append((dep.dep, dep))
            if token == dep.dep and dep not in route:
                where_to_go.append((dep.gov, dep))        

        #If max_len less than 2 return our findings
        routes = []
        if max_len == 1:
            for start_token, dep in where_to_go:
                routes.append(route + [dep])
            return routes

        #Otherwise, we'll get more routes
        for start_token, dep in where_to_go:
            routes.extend(self.get_token_tree_context(start_token, max_len=max_len - 1, route=route + [dep]))

        return routes

    def get_route_in_tree(self, start, target, route=[]):

        #Get every dep in which current token is mentioned
        where_to_go = []
        for dep in self.deps:
            if start == dep.gov and dep not in route:
                if dep.dep == target:
                    #Found it!
                    route.append(dep)
                    return route
                where_to_go.append((dep.dep, dep))
            if start == dep.dep and dep not in route:
                if dep.gov == target:
                    #Found it!
                    route.append(dep)
                    return route
                where_to_go.append((dep.gov, dep))

        if len(where_to_go) == 0:
            return []

        for start_token, dep in where_to_go:
            result = self.get_route_in_tree(start_token, target, route=route + [dep])
            if result != []:
                return result
        return []

    def create_token_routes(self):
        #This is for emergency use only!
        self.routes = {}
        for t in self.tokens:
            if t not in self.routes.keys():
                self.routes[t] = {}
            for tt in self.tokens:
                if t != tt:
                    self.routes[t][tt] = self.get_route_in_tree(t, tt)

    def create_context_routes(self):
        #This is quite likely not very optimal
        self.context = {}
        for t in self.tokens:
            self.context[t] = self.get_token_tree_context(t, max_len=3)


class Token(object):

    def __init__(self,idx,text,pos="",feat="",lemma=""):
        self.index=idx
        self.text=text
        self.pos=pos
        self.feat=feat
        self.lemma=lemma
        self.is_semeval_root=False

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


