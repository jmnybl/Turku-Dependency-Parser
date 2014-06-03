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

def test1():
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

def test2():
    state=PerceptronSharedState(40)
    gp1=GPerceptron.from_shared_state(state)
    gp2=GPerceptron.from_shared_state(state)
    gp3=GPerceptron.from_shared_state(state)
    print "GP1"
    print gp1.w
    print gp1.w_avg
    print gp1.w_avg_N
    print "-------------------------"
    gp1.update({"X":1.0, "Y":1.0},{"X":1.0,"Z":1.0},0.2,0.1,0.0)
    print gp1.w
    print gp1.w_avg
    print gp1.w_avg_N
    print
    print
    print "GP2"
    print gp2.w
    print gp2.w_avg
    print gp2.w_avg_N
    print "-------------------------"
    gp2.update({"X":1.0, "Y":1.0},{"X":1.0,"Z":1.0},0.2,0.1,0.0)
    print gp2.w
    print gp2.w_avg
    print gp2.w_avg_N
    print
    print
    print "GP3"
    print gp3.w
    print gp3.w_avg
    print gp3.w_avg_N
    print "-------------------------"
    gp3.update({"X":1.0, "Y":1.0},{"X":1.0,"Z":1.0},0.2,0.1,0.0)
    print gp3.w
    print gp3.w_avg
    print gp3.w_avg_N
    print
    print
    print "************* RELOAD *************"
    state.save("delme.s",True)
    state=PerceptronSharedState.load("delme.s",True)
    gp1=GPerceptron.from_shared_state(state)
    print gp1.w
    print gp1.w_avg
    print gp1.w_avg_N
    

test2()
    
