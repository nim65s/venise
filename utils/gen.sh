#!/bin/bash

cd ~/ubi

for f in *
do
    if [[ -d $f ]]
    then
        echo $f
        cd $f
        [[ -f 1 ]] || grep ArbreC1 * |sort > 1
        [[ -f 2 ]] || grep ArbreC2 * |sort > 2
        [[ -f 3 ]] || grep ArbreC3 * |sort > 3
        cd ..
    fi
done
