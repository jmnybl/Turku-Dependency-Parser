from perceptron import PerceptronSharedState, GPerceptron
import multiprocessing
import time
import random

#Trivial little test of the perceptron


class DataGen(object):
    #Generate data from a random distribution

    def __init__(self,N):
        #N is dimensionality
        self.means=[(random.random()*2.0)-1.0 for _ in range(N)]
        self.stds=[(random.random()*2.0) for _ in range(N)]

    def draw(self):
        #Returns a dictionary of features
        d={}
        for idx in range(len(self.means)):
            if random.random()<0.99:
                pass #skip 99% of the features to make this a bit sparser
            d["f"+str(idx)]=random.normalvariate(self.means[idx],self.stds[idx])
        return d

def one_process(gp,dist1,dist2):
    #Gets one generalized perceptron to work with

    #Draw two points and see if they get ranked correctly
    countPositive=0
    countTotal=0
    while True:
        d1=dist1.draw()
        d2=dist2.draw()
        s1=gp.score(d1) #"GS"
        s2=gp.score(d2) #"SYS"
        countTotal+=1
        if s1>s2:
            countPositive+=1
            #all okay, do nothing
            pass
        else:
            print "Update", float(countPositive)/countTotal
            gp.update(d2,d1,s2,s1)
#This is created in the main process

state=PerceptronSharedState(10000)
dist1=DataGen(1000)
dist2=DataGen(1000)
PS=[]
for x in range(8):
    newGP=GPerceptron.from_shared_state(state)
    p=multiprocessing.Process(target=one_process,args=(newGP,dist1,dist2))
    p.start()
    PS.append(p)

for p in PS:
    p.join()

print state.w_avg_N_s.value
state.save("xxx2",True)
