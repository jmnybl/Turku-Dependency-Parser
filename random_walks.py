import conllutil
import sys
import codecs
import numpy
import argparse
import gzip

inf=99999 # ...integer to represent inf

conllu_columns={u"FORM":conllutil.FORM,u"LEMMA":conllutil.LEMMA,u"POS":conllutil.CPOS,u"FEAT":conllutil.FEAT,u"DEPREL":conllutil.DEPREL}

class Graph(object):

    @classmethod
    def create_from_conllu(cls,sent):
        """ This is the way to create graphs! """
        g=cls()
        g.length=len(sent)
        for i in range(0,len(sent)):
            gov=int(sent[i][conllutil.HEAD])-1
            if gov==-1:
                continue
            g.edges.append((gov,i))
            g.weights[(gov,i)]=1
        return g

    def __init__(self):
        """ Initialize empty, everything indexed as integers """
        self.length=0
        self.edges=[] # (g,d) tuples
        self.weights={} # key:(g,d) tuples, value:int
        self.dist=None
        self.next=None


    def path(self,i,j):
        """ Reconstruct the shortest path between i and j. Return list of integers (token indices). """
        if i==j:
            return [i]
        if self.next[i][j]==-1:
            raise NameError("No path between i and j.")
        intermediate=self.next[i][j]
        return self.path(i,intermediate) + [j]


    def floydWarshall(self):
        """ Floyd-Warshall algorithm to find all-pairs shortest paths. """
        if self.dist is not None and self.next is not None: # ...we already have these
            return
        size=self.length
        # init dist array
        dist=numpy.empty([size,size],dtype=int)
        dist.fill(inf)
        for i in xrange(0,size):
            dist[i][i]=0
        for u,v in self.edges:
            dist[u][v]=self.weights[(u,v)] # the weight of the edge (u,v)
            dist[v][u]=self.weights[(u,v)] # this will treat the graph as undirected
        # init next array
        next=numpy.empty([size,size],dtype=int)
        next.fill(inf)
        for i in xrange(0, size):
            for j in xrange(0, size):
                if i==j or dist[i][j]==inf:
                    next[i][j]=-1
                else:
                    next[i][j]=i
        for k in xrange(0, size):
            for i in xrange(0, size):
                for j in xrange(0, size):
                    if dist[i][j]>dist[i][k]+dist[k][j]:
                        dist[i][j]=dist[i][k]+dist[k][j]
                        next[i][j]=next[k][j]
        self.dist=dist
        self.next=next


def print_walk(path,field,out):
    fields=field.split(u"|")
    def get_field(l):
        return u"|".join(l[conllu_columns[f]] for f in fields)
    print >> out, (u" ".join(get_field(sent[t]) for t in path)).encode(u"utf-8")



if __name__==u"__main__":

    parser = argparse.ArgumentParser()
    g=parser.add_argument_group()
    g.add_argument('--column', default=u"ALL", help='FORM, LEMMA, POS, FEAT or DEPREL, or their combination like POS|FEAT. ALL means "the usual suspects" written to files XXX_randwalks_NNNN.txt.gz (default ALL)')
    g.add_argument('-m', '--max', type=int, default=10000, help='How many sentences, 0 for all (default 10000)')
    args = parser.parse_args()

    if args.column=="ALL":
        outputs=[['POS',"POS_randwalks_%(size)d.txt.gz"],['FEAT',"FEAT_randwalks_%(size)d.txt.gz"],['POS|FEAT',"POS_FEAT_randwalks_%(size)d.txt.gz"]]
    else:
        outputs=[(args.column,args.column.replace(u"|","_")+"_randwalks_%(size)d.txt.gz")]

    for o in outputs:
        o[1]=gzip.open(o[1]%{"size":args.max},"w")

    counter=0
    for comm,sent in conllutil.read_conllu(codecs.getreader(u"utf-8")(sys.stdin)):

        if len(sent)==1: # ...no need for single token sentences
            continue

        if len(sent[0])>10: # conll09 --> conllu
            sent=conllutil.conll09_to_conllu_no_features(sent)

        graph=Graph.create_from_conllu(sent)
        graph.floydWarshall()

        # create all walks
        for i in range(0,graph.length):
            for j in range(i+1,graph.length): # we can treat this as a triangular matrix
                if graph.dist[i][j]==inf: # ...no path found, incorrect tree
                    continue
                path=graph.path(i,j)                
                for col,o in outputs:
                    print_walk(path,col,o)
        
        counter+=1
        if args.max!=0 and counter>=args.max:
            break

    print >> sys.stderr, counter
    for col,o in outputs:
        o.close()





