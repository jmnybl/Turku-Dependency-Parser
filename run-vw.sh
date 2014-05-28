killall spanning_tree
spanning_tree

COUNTER=0
TOTAL=$(ls /usr/share/ParseBank/pbv3.part-*.gz | wc -l)
LAST=$(( $TOTAL - 1))
for fName in  /usr/share/ParseBank/pbv3.part-*.gz
do
    CMD="vw --total $TOTAL --node $COUNTER --unique_id 123 --passes 1 --span_server localhost --oaa 94 -b 26 --progress 30000 --holdout_off  -l 0.5 --initial_t 1.0"
    if [[ $COUNTER -eq $LAST ]]
    then
	zcat $fName | python train_vw.py 2> log/onode_$COUNTER | $CMD -f trained-tdt-jennaf.vw > log/node_$COUNTER 2>&1
    else
	zcat $fName | python train_vw.py 2> log/onode_$COUNTER | $CMD > log/node_$COUNTER 2>&1 &
    fi
    COUNTER=$(( $COUNTER + 1 ))
done
