import codecs
import sys
import os
import argparse

SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))

def read_conll(inp,maxsent):
    """ Read conll format file and yield one sentence at a time as a list of lists of columns. If inp is a string it will be interpreted as filename, otherwise as open file for reading in unicode"""
    if isinstance(inp,basestring):
        f=codecs.open(inp,u"rt",u"utf-8")
    else:
        f=codecs.getreader("utf-8")(sys.stdin) # read stdin
    count=0
    sent=[]
    comments=[]
    for line in f:
        line=line.strip()
        if not line:
            if sent:
                count+=1
                yield sent, comments
                if maxsent!=0 and count>=maxsent:
                    break
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

header=u'<div class="sd-parse">\n'
footer=u'</div>\n'


def conll2sddep(sent):
    """ Transforms graph into sd-dep format brat supports. """
    sd=[]
    sd.append(header)
    sd.append(u" ".join(token[1] for token in sent))
    pred_count=0
    for i in xrange(len(sent)):
        if sent[i][5]==u"+": # predicate
            pred_count+=1
            for j in xrange(len(sent)):
                if sent[j][5+pred_count]!=u"_": # argument
                    dep=u"%s(%s,%s)"%(sent[j][5+pred_count],sent[i][1],sent[j][1])
                    sd.append(dep)
    sd.append(footer)
    return sd


def visualize(args):
    data_to_print=u""
    for sent,comments in read_conll(args.input,args.max_sent):
        sd=conll2sddep(sent)
        tree=u"\n".join(l for l in sd)
        data_to_print+=tree
    with codecs.open(os.path.join(SCRIPTDIR,u"templates","simple_brat_viz.html"),u"r",u"utf-8") as template:
        data=template.read().replace(u"CONTENTGOESHERE",data_to_print,1)
        print >> sys.stdout, data.encode(u"utf-8")


if __name__==u"__main__":

    parser = argparse.ArgumentParser(description='Trains the parser in a multi-core setting.')
    g=parser.add_argument_group("Input/Output")
    g.add_argument('input', nargs='?', help='Parser output file name, or nothing for reading on stdin')
    g.add_argument('--max_sent', type=int, default=0, help='How many trees to show? 0 for all. (default %(default)d)')
    args = parser.parse_args()
    visualize(args)
