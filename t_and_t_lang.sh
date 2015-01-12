LANG=$1
CPUs=$2
BEAM=$3
shift 3

mkdir -p out

python train_parallel.py -p $CPUs --cpu-aff --beam $BEAM $* -o model.$LANG.taito.b$BEAM semeval_data/train.$LANG.conllu 

exit


# PARSER_PID=$!

# while [[ 1 ]]
# do
#     #Check for new models
#     for M in model.$LANG.taito.b$BEAM.i*
#     do
# 	if [[ ! -f out/devel.$M.st_format && -f $M]]
# 	then
# 	    echo "New model $M"
# 	    #New model! Parse it!
# 	    #..stop training
# 	    kill -s SIGSTOP $PARSER_PID
# 	    python parse_parallel -p $CPUs --cpu-aff $M semeval_data/devel.$L.conllu > out/devel.$M.conllu
# 	    python seval2tree.py -r < out/devel.$M.conllu > out/devel.$M.stformat
# 	    kill - SIGCONT $PARSER_PID
# 	fi
#     done
#     #Has the parser finished?
#     ps -p $PARSER_PID > /dev/null
#     if [[ $? ]]
#     then
# 	exit
#     fi
#     sleep 10 #...try again in 10s
# done

