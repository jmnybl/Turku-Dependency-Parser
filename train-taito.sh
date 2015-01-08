#!/bin/bash
CPUs=9

echo "sbatch -t 24:0:0 -N1 --ntasks-per-node=1 -c$CPUs -e b10_lin.err -o b10_lin.out --mem-per-cpu=800 --wrap 'python train_parallel.py -p $CPUs --cpu-aff --beam 10 -o model.dm.taito.b10 semeval_data/train_dm_trees.conll'"

