import codecs
import sys
import glob
import gzip
import threading

#tehokas/A/amod/2 agentti/N/appos/0 owen/N/appos/2 )/Punct/punct/3

form=u"%(ID)d %(FORM)s %(LEMMA)s _ %(POS)s _ %(FEAT)s _ %(HEAD)s _ %(DEPREL)s _ _ _ _".replace(u" ",u"\t")

def ng2conll(ng,out):
    tokens=[]
    for idx,tok in enumerate(ng.split()):
        wform,pos,rel,head=tok.rsplit(u"/",3)
        print >> out, form%{u"ID":idx+1,u"FORM":wform,u"POS":pos,u"FEAT":u"_",u"HEAD":head,u"DEPREL":rel,u"LEMMA":u"_"}

def process_one_file(fname,out,lock):
    f=gzip.open(fname,"r")
    for line in codecs.getreader("utf-8")(f):
        line=line.strip()
        if not line:
            continue
        head,ng,count,year=line.split(u"\t")
        lock.acquire()
        print >> out, u"# count:",count
        ng2conll(ng,out)
        print >> out
        out.flush()
        lock.release()
    f.close()

if __name__=="__main__":
    # A bunch of individually shuffled ngram files of roughly the same size
    # Let's read them all at once and
    # compete for stdout, which will merge them quite well, hopefully
    files=glob.glob("/mnt/ssd/w2v_sng_training/triarcs-repacked-uniq/fin-triarcs-uniq-*.gz")
    out=codecs.getwriter("utf-8")(sys.stdout)
    #Lock for stdout
    lock=threading.Lock()
    threads=[]
    for f in files:
        #Launch a thread for every file
        t=threading.Thread(target=process_one_file,args=(f,out,lock))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()



