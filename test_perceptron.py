from perceptron import PerceptronSharedState, GPerceptron
import multiprocessing
import time

#This is created in the main process
state=PerceptronSharedState(5000000)

def one_process(gp):
    #Gets one generalized perceptron to work with
    #...of course this will then do the updates and what not...
    with gp.w_avg_N.get_lock():
        gp.w_avg_N.value+=1.0

PS=[]
for x in range(25):
    newGP=GPerceptron.from_shared_state(state)
    p=multiprocessing.Process(target=one_process,args=(newGP,))
    p.start()
    PS.append(p)

for p in PS:
    p.join()

print state.w_avg_N_s.value
