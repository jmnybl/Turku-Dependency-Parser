#!/bin/bash

#Call with no args for all languages or
#./train-taito.sh cs.psd en.psd
#for example


CPUs=13
BEAM=10

if [[ ! $1 ]]
then
    LANGS="cs.psd en.dm en.pas en.psd"
else
    LANGS="$*"
fi

for L in $LANGS
do
    if [[ "$L" == "cs.psd" || "$L" == "en.psd" ]]
    then
	DS=0.15
    else
	DS=0.3
    fi
    echo "sbatch -t 36:0:0 -N1 --ntasks-per-node=1 -J $L -c$CPUs -e log/$L.err -o log/$L.out --mem-per-cpu=800 --wrap './t_and_t_lang.sh $L $CPUs $BEAM --downsample=$DS'"
done
