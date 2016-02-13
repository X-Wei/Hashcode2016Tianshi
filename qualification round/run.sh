#!/bin/bash

#~ for i in $(seq 1 100)
#~ do
    #~ echo "busy-$i..."
    #~ cat busy_day.in | python drone.py > proba/busy$i
    #~ echo "mother-$i..."
    #~ cat mother_of_all_warehouses.in | python drone.py > proba/mother$i
    #~ echo "red-$i..."
    #~ cat redundancy.in | python drone.py > proba/red$i
#~ done

for name in busy mother red
do
    for i in $(seq 1 100)
    do
        echo "$name$i:\t$(head -n1 proba/$name$i)"
    done
done

#~ declare -i max_score
#~ declare -i score
#~ for name in busy mother red
#~ do
    #~ max = 0
    #~ for i in $(seq 1 2)
    #~ do
        #~ score=$(head -n1 proba/$name$i)
        #~ if [ $score -gt $max_score ]
        #~ then
            #~ max_score = score
            #~ echo "$name$i:\t$max_score"
        #~ fi
    #~ done
#~ done
