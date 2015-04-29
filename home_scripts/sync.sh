#!/bin/bash

for h in moro ame yuki
do
    rsync -avP --exclude='*.pyc' --exclude='*.orig' venise $h: &
done

wait

for h in moro ame yuki
do
    ssh $h 'rm -f venise/**.pyc venise/**.orig'
done
