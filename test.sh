#!/bin/bash -l
#SBATCH -J tst
#SBATCH -o log/e.out
#SBATCH -e log/e.err
#SBATCH -t 03:00:00
#SBATCH -p serial
#SBATCH -c 8
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem-per-cpu=800


indir=$1

CPUS=8

mkdir -p ev

for lang in cs.psd en.dm en.pas en.psd
do
    for m in $indir/model.$lang.taito.*
    do
	mbase=`basename $m`
	out=ev/$mbase.small.conllu
	if [[ -e $m && ! -e $out ]]
	then
	    python parse_parallel.py -p $CPUS --cpu $m semeval_data/devel.small.$lang.conllu > $out
	    python seval2tree.py -r < $out > ev/$mbase.small.out
	fi
    done
done
