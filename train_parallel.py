import multiprocessing
import argparse
import os
import perceptron
import codecs
import sys
import StringIO
import tparser

def one_process(g_perceptron,q):
    """
    g_perceptron - instance of generalized perceptron (not state)
    q - queue with examples
    """
    parser=tparser.Parser(gp=g_perceptron)
    while True:
        next_job=q.get() #This will be either (progress,data) tuple, or None to signal end of training
        if next_job==None:
            return #We're done
        progress,data=next_job
        buff=StringIO.StringIO(data) #Make the input look like an open file reading unicode
        parser.train(inp=buff,progress=progress)

def feed_queue(q,inp,iteration_progress=0.0,max_sent=0):
    """iteration_progress -> progress through the total number of iterations, will be passed on to the parser"""
    if inp==None: #Do stdin
        data=codecs.getreader("utf-8")(sys.stdin)
    else:
        data=codecs.open(inp,"rt","utf-8")

    counter=0
    ### WARNING: comments are not correctly paired with sentences -> if you communicate metadata through comments, this will need to be fixed
    current=[] #List of lines waiting to be scheduled
    for line in data:
        if line.startswith(u"1\t"):
            counter+=1
            if counter%20==0: #Split the queue into batches of 20 sentences to train on
                q.put((iteration_progress,u"".join(current)))
                current=[]
            if max_sent!=0 and counter>=max_sent:
                break
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
    q=multiprocessing.Queue(20)  #Queue to pass pieces of the training data to the processes

    procs=[] #List of running processes
    for _ in range(args.processes):
        gp=perceptron.GPerceptron.from_shared_state(sh_state) #Fork a new perceptron
        p=multiprocessing.Process(target=one_process, args=(gp,q))
        p.start()
        procs.append(p)

    #All processes started
    #...feed the queue with data
    for i in range(args.iterations):
        feed_queue(q,args.input,float(i)/args.iterations,args.max_sent)

    #Signal end of work to all processes (Thanks @radimrehurek for this neat trick!)
    for _ in range(args.processes):
        q.put(None) 
    
    for p in procs:
        p.join() #Wait for the processes to quit
    
    #...and we should be done
    sh_state.save(args.output,True)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Train')
    parser.add_argument('-p', '--processes', type=int, default=4, help='How many processes to run? (default %(default)d)')
    parser.add_argument('--max_sent', type=int, default=0, help='How many sentences to read from the input? 0 for all.  (default %(default)d)')
    parser.add_argument('-i', '--iterations', type=int, default=10, help='How many iterations to run? (default %(default)d)')
    parser.add_argument('--dim', type=int, default=5000000, help='Dimensionality of the trained vector. (default %(default)d)')
    parser.add_argument('-o', '--output', required=True, help='Name of the output model.')
    parser.add_argument('input', nargs='?', help='Training file name, or nothing for training on stdin')
    args = parser.parse_args()

    if args.iterations>1 and args.input==None:
        print >> sys.stderr, "If you want more than one iteration, you will need to give the training data as a file, not on stdin"
        sys.exit(1)
    
    launch_instances(args)
