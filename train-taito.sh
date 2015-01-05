#!/bin/bash
CPUs=10

echo "sbatch -t 24:0:0 -n 1 --ntasks-per-node 1 -c $CPUs -e b10.err -o b10.out --mem-per-cpu=800 --wrap 'python train_parallel.py -p $CPUs --beam 10 -o model.dm.taito.b10 semeval_data/train_dm_trees.conll'"

