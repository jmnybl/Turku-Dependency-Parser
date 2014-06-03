killall spanning_tree
spanning_tree

NICE=19
COUNTER=0
TOTAL=$(ls /usr/share/ParseBank/pbv3.part-*.gz | wc -l)
LAST=$(( $TOTAL - 1))
for fName in  /usr/share/ParseBank/pbv3.part-*.gz
do
    CMD="vw --total $TOTAL --node $COUNTER --unique_id 123 --passes 1 --span_server localhost --oaa 94 -b 26 --progress 30000 --holdout_off  -l 0.5 --initial_t 1.0"
    if [[ $COUNTER -eq $LAST ]]
    then
	nice -n $NICE zcat $fName | nice -n $NICE python train_vw.py 2> log/onode_$COUNTER | nice -n $NICE $CMD -f trained-pb.vw > log/node_$COUNTER 2>&1
    else
	nice -n $NICE zcat $fName | nice -n $NICE python train_vw.py 2> log/onode_$COUNTER | nice -n $NICE $CMD > log/node_$COUNTER 2>&1 &
    fi
    COUNTER=$(( $COUNTER + 1 ))
done

