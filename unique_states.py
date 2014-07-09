import logging
logging.basicConfig(format="%(asctime)-15s  %(message)s",level=logging.INFO)

import argparse
import sys
import codecs
import tree, tparser

out=codecs.getwriter("utf-8")(sys.stdout)

def print_state(state,args):
    print >> out,  u"%d/%d"%(len(state.stack[-2:]),len(state.queue[:3])),
    print >> out,  u"\t",
    print >> out,  u"\t".join(t.text for t in state.stack[-2:]),
    print >> out,  u"\t",
    print >> out,  u"\t".join(t.text for t in state.queue[:3])

def emit_states(args):
    parser=tparser.Parser()
    if args.input==None:
        inp=codecs.getreader("utf-8")(sys.stdin)
    else:
        inp=codecs.open(args.input,"r","utf-8")

    failed=0
    for counter,sent in enumerate(tree.read_conll(inp)):
        if counter%1000==0:
            logging.info("Processed %d total with %d failed."%(counter,failed))
        gs_tree=tree.Tree.new_from_conll(conll=sent,syn=True)
        non_projs=gs_tree.is_nonprojective()
        if len(non_projs)>0:
            gs_tree.define_projective_order(non_projs)
        try:
            gs_transitions=parser.extract_transitions(gs_tree,sent)
        except ValueError:
            failed+=1
            continue
        gs_state=tparser.State(sent,syn=False)
        while not gs_state.tree.ready:
            gs_trans=gs_transitions[len(gs_state.transitions)]
            print_state(gs_state,args)
            gs_state.update(gs_trans)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Emits parser states.')
    g=parser.add_argument_group("Input/Output")
    g.add_argument('input', nargs='?', help='Training file name, or nothing for training on stdin')
    args = parser.parse_args()
    emit_states(args)


    
