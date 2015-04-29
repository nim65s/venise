#!/bin/bash

for h in moro ame yuki
do
    rsync -avP --exclude='*.pyc' --exclude='*.orig' --exclude='__pycache__' venise $h: &
done

wait

for h in moro ame yuki
do
    ssh $h 'rm -f venise/**.pyc venise/**.orig'
    ssh $h 'sudo systemctl restart agv'
done
