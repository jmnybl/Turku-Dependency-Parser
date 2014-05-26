for f in /usr/share/ParseBank/pbv3.part-*.gz
do
    zcat $f | python train_vw.py  > out/$(basename $f).vwdata 2> out/$(basename $f).vwdata.log &
done 

for job in `jobs -p`
do
    echo $job
    wait $job
done
