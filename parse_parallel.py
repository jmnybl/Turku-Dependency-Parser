import multiprocessing
import argparse
import os
import perceptron
import codecs
import sys
import StringIO
import tparser
import time
import json

def one_process(model_file_name,g_perceptron,q,q_out,parser_config,no_avg):
    """
    g_perceptron - instance of generalized perceptron (not state)
    q - queue with examples
    job_counter - synchronizes the jobs for printing
    parser_config - holds information about the beam size used during training
    no_avg - do not use averaged weight vector (so, test_time=False)
    """
    if no_avg:
        parser=tparser.Parser(model_file_name,gp=g_perceptron,beam_size=parser_config["beam_size"],test_time=False)
    else:
        parser=tparser.Parser(model_file_name,gp=g_perceptron,beam_size=parser_config["beam_size"],test_time=True)
    while True:
        next_job=q.get() #This will be either (progress,data) tuple, or None to signal end of training
        if next_job==None:
            break #We're done
        job_number,data=next_job
        buffIN=StringIO.StringIO(data) #Make the input look like an open file reading unicode
        buffOUT=StringIO.StringIO()
        parser.parse(buffIN,buffOUT)
        #Done, push out
        q_out.put((job_number,buffOUT.getvalue().encode("utf-8")))
    q_out.put(None) #Signal downstream that we're done

def assemble_results(qout,parsers_alive):
    cache={} #{jobid:txt}
    counter=0
    while True:
        if parsers_alive>0:
            next_job=qout.get()
            if next_job==None:
                parsers_alive-=1 #Another one done
            else:
                job_number,data=next_job
                assert job_number not in cache
                cache[job_number]=data
        #Print everything you can
        while counter in cache:
            print cache[counter]
            del cache[counter]
            counter+=1
        if parsers_alive==0 and not cache: #DOne
            return


def feed_queue(q,inp,max_sent=0):
    """iteration_progress -> progress through the total number of iterations, will be passed on to the parser"""
    if inp==None: #Do stdin
        data=codecs.getreader("utf-8")(sys.stdin)
    else:
        data=codecs.open(inp,"rt","utf-8")

    job_counter=0
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
            if counter%5==0: #Split the queue into batches of 20 sentences to train on
                q.put((job_counter,u"".join(current)))
                job_counter+=1
                current=[]
            if max_sent!=0 and counter>=max_sent:
                break
            for comm in comments:
                current.append(comm)
            comments=[]
        current.append(line)
    else:
        if current:
            q.put((job_counter,u"".join(current)))
            
    if inp!=None:
        data.close() #Close what you opened

def launch_instances(args):
    """
    main() to launch everything
    """
    
    #1) Create the Shared State for perceptron
    # TODO: maybe I could have a flag with which I'd check the model exists and load instead?
    #      ...will overwrite by default anyway

    sh_state=perceptron.PerceptronSharedState.load(args.model[0],retrainable=True)
    
    # now load parser configuration to get correct beam size
    if not os.path.exists(args.model[0]):
        raise ValueError(args.model[0]+": no such model")
    with open(os.path.join(args.model[0],"parser_config.json"),"r") as f:
        d=json.load(f) #dictionary with parameters

    q=multiprocessing.Queue(20)  #Queue to pass pieces of the training data to the processes
    q_out=multiprocessing.Queue(20) #Queue to pass parsed data to the process which assembles the parsed output

    procs=[] #List of running processes
    for _ in range(args.processes):
        gp=perceptron.GPerceptron.from_shared_state(sh_state) #Fork a new perceptron
        p=multiprocessing.Process(target=one_process, args=(os.path.join(args.model[0],"model.pkl"),gp,q,q_out,d,args.no_avg))
        p.start()
        procs.append(p)
    p=multiprocessing.Process(target=assemble_results,args=(q_out,args.processes))
    p.start()
    procs.append(p)

    #All processes started
    #...feed the queue with data
    feed_queue(q,args.input,args.max_sent)

    #Signal end of work to all processes (Thanks @radimrehurek for this neat trick!)
    for _ in range(args.processes):
        q.put(None) 
    
    for p in procs:
        p.join() #Wait for the processes to quit
    
    #...and we should be done


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Runs the parser in a multi-core setting. Outputs to stdout.')
    parser.add_argument('model', nargs=1, help='Name of the model file.')
    parser.add_argument('input', nargs='?', help='Training file name, or nothing for training on stdin')
    parser.add_argument('-p', '--processes', type=int, default=4, help='How many parsing workers to run? (default %(default)d)')
    parser.add_argument('--max_sent', type=int, default=0, help='How many sentences to parse from the input? 0 for all.  (default %(default)d)')
    parser.add_argument('--no_avg', default=False, action="store_true",  help='Do not use the averaged perceptron but the original weight vector (default %(default)s)')
    parser.add_argument('--cpu-affinity',default=False,action="store_true",help="If all processes only end up using a single core, specify this parameter to reset any CPU affinity restrictions. This is necessary e.g. on the CSC RHEL cluster.")

    args = parser.parse_args()

    if args.cpu_affinity:
        os.system("taskset -p 0xff %d" % os.getpid())

    launch_instances(args)
