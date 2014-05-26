COUNTER=0
TOTAL=$(ls TDT/tdt-train-part.*.vwdata | wc -l)
LAST=$(( $TOTAL - 1))
for fName in TDT/tdt-train-part.*.vwdata
do
    CMD="vw --total $TOTAL --node $COUNTER --unique_id 123 -q QS -q QQ -q SS -q Qs -q qS --passes 25 -d $fName --span_server localhost --oaa 94 -b 26 -c --progress 10000 --holdout_off --save_resume --examples 30000000 --save_per_pass"
    #CMD="vw --total $TOTAL --node $COUNTER --unique_id 123 -q QS -q QQ -q SS -q Qs -q qS --passes 2 -d $fName --span_server localhost -b 26 -c --progress 20000 --holdout_off --save_resume --examples 30000000 --save_per_pass -i trained.vw.30M.round0 "
    if [[ $COUNTER -eq $LAST ]]
    then
	$CMD -f trained-tdt.vw > log/node_$COUNTER 2>&1
    else
	$CMD > log/node_$COUNTER 2>&1 &
    fi
    COUNTER=$(( $COUNTER + 1 ))
done
