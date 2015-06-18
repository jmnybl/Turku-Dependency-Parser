from __future__ import division
import sys
import codecs

ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

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

import argparse
 
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='LAS')
    parser.add_argument('gs', nargs=1, help='GS')
    parser.add_argument('sys', nargs=1, help='SYS')
    args = parser.parse_args()
    trees_gs=list(read_conll(args.gs[0],0))
    trees_sys=list(read_conll(args.sys[0],0))
    
    assert len(trees_gs)==len(trees_sys)
    
    LAS=0
    UAS=0
    TOTAL=0

    for (gs_tree,gs_comments),(sys_tree,sys_comments) in zip(trees_gs,trees_sys):
        assert len(gs_tree)==len(sys_tree)
        for gs_line,sys_line in zip(gs_tree,sys_tree):
            TOTAL+=1
            if gs_line[HEAD]==sys_line[HEAD]:
                UAS+=1
                if gs_line[DEPREL]==sys_line[DEPREL]:
                    LAS+=1
    print "LAS=%.1f  UAS=%.1f   TOTAL=%d"%(LAS/TOTAL*100,UAS/TOTAL*100,TOTAL)
    
