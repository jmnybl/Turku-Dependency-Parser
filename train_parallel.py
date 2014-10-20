import multiprocessing
import argparse
import os
import perceptron
import codecs
import sys
import StringIO
import tparser
import json
import time
import threading

def one_process(g_perceptron,q,beam_size):
    """
    g_perceptron - instance of generalized perceptron (not state)
    q - queue with examples
    beam_size - size of the beam to be passed to the parser instance
    """
    parser=tparser.Parser(gp=g_perceptron,beam_size=beam_size)
    while True:
        next_job=q.get() #This will be either (progress,data) tuple, or None to signal end of training
        if next_job==None:
            return #We're done
        progress,data=next_job
        buff=StringIO.StringIO(data) #Make the input look like an open file reading unicode
        parser.train(inp=buff,progress=progress)

def feed_queue(q,inp,iteration_progress=0.0,max_sent=0):
    """iteration_progress -> progress through the total number of iterations, will be passed on to the parser.
    """
    if inp==None: #Do stdin
        data=codecs.getreader("utf-8")(sys.stdin)
    else:
        data=codecs.open(inp,"rt","utf-8")

    counter=0
    ### WARNING: comments are not correctly paired with sentences -> if you communicate metadata through comments, this will need to be fixed
    comments=[]
    current=[] #List of lines waiting to be scheduled
    for line in data:
        if line.startswith(u"#"):
            comments.append(line)
            continue
        if line.startswith(u"1\t"):
            counter+=1
            if counter%40==0: #Split the queue into batches of 40 sentences to train on
                q.put((iteration_progress,u"".join(current)))
                current=[]
            if max_sent!=0 and counter>=max_sent:
                break
            for comm in comments:
                current.append(comm)
            comments=[]
        current.append(line)
    else:
        if current:
            q.put((iteration_progress,u"".join(current)))
            
    if inp!=None:
        data.close() #Close what you opened

def launch_instances(args):
    """
    main() to launch everything
    """

    #1) Create the Shared State for perceptron
    # TODO: maybe I could have a flag with which I'd check the model exists and load instead?
    #      ...will overwrite by default anyway
 
    sh_state=perceptron.PerceptronSharedState(w_len=args.dim)
    q=multiprocessing.Queue(30)  #Queue to pass pieces of the training data to the processes

    procs=[] #List of running processes
    for _ in range(args.processes):
        gp=perceptron.GPerceptron.from_shared_state(sh_state) #Fork a new perceptron
        p=multiprocessing.Process(target=one_process, args=(gp,q,args.beam_size))
        p.start()
        procs.append(p)

    #Regular save
    done=threading.Event()
    iteration_number_as_list=[0] #Just a handy-dandy way to communicate the number into the reg. save thread without global variable
    if args.save_every_min>0: #We'll be running regular save
        p=threading.Thread(target=regular_save,args=(sh_state,args,iteration_number_as_list,done))
        p.start()

    #All processes started
    #...feed the queue with data
    for iteration_number in range(args.iterations):
        iteration_number_as_list[0]=iteration_number
        feed_queue(q,args.input,float(iteration_number)/args.iterations,args.max_sent)
        #Iteration ended, store if you are supposed to, unless it's the last iteration
        if args.save_per_iter and iteration_number<args.iterations-1: 
            save_model(sh_state,args,iteration_number)

    #Signal end of work to all processes (Thanks @radimrehurek for this neat trick!)
    for _ in range(args.processes):
        q.put(None) 
    
    for p in procs:
        p.join() #Wait for the processes to quit
    
    done.set() #tells the regular save process to finish

    #...and we should be done
    save_model(sh_state,args,None)

def save_model(sh_state,args,iteration_number=None):
    """
    Save the model. If iteration_number is an integer, save it numbered
    """
    if iteration_number!=None:
        oName=args.output+(".i%02d"%iteration_number)
    else:
        oName=args.output
    sh_state.save(oName,True)
    d={"beam_size":args.beam_size}
    with open(os.path.join(oName,"parser_config.json"),"w") as f: # save also parser configuration, currently only beam size
        json.dump(d,f)

def regular_save(sh_state,args,iteration_number_aslist,done):
    """Save at regular intervals, watch for the done Event, and exit if it is set"""
    counter=0 #counts seconds since started
    next_save=args.save_every_min*60 #counter value for the next save
    while True:
        time.sleep(1)
        if done.is_set():
            return
        if counter>next_save:
            print >> sys.stderr, "NEXT SAVE"
            sys.stderr.flush()
            save_model(sh_state,args,iteration_number_aslist[0])
            next_save+=args.save_every_min*60
        counter+=1
        
    

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Trains the parser in a multi-core setting.')
    g=parser.add_argument_group("Input/Output")
    g.add_argument('input', nargs='?', help='Training file name, or nothing for training on stdin')
    g.add_argument('-o', '--output', required=True, help='Name of the output model.')
    g.add_argument('--no_save_per_iter', required=False, dest='save_per_iter', action="store_false", default=True, help='Do not save the model after every iteration, with a ".iNN". Do it by default.')
    g.add_argument('--save_every_min', required=False, dest='save_every_min', action="store", default=0, type=int, help='Save the model every N minutes, overwriting the previous one. Default %(default)s - off.')
    g=parser.add_argument_group("Training config")
    g.add_argument('-p', '--processes', type=int, default=4, help='How many training workers to run? (default %(default)d)')
    g.add_argument('--max_sent', type=int, default=0, help='How many sentences to read from the input? 0 for all.  (default %(default)d)')
    g=parser.add_argument_group("Training algorithm choices")
    g.add_argument('-i', '--iterations', type=int, default=10, help='How many iterations to run? If you want more than one, you must give the input as a file. (default %(default)d)')
    g.add_argument('--dim', type=int, default=5000000, help='Dimensionality of the trained vector. (default %(default)d)')
    g.add_argument('--beam_size', type=int, default=40, help='Size of the beam. (default %(default)d)')
    args = parser.parse_args()

    if args.iterations>1 and args.input==None:
        print >> sys.stderr, "If you want more than one iteration, you will need to give the training data as a file, not on stdin"
        sys.exit(1)
    
    launch_instances(args)
