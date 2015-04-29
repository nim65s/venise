#!/bin/bash

./sync.sh

for h in moro ame yuki
do
    (
    ssh $h 'cd /etc/systemd/system; sudo cp /home/pi/venise/conf/*.service .'
    ssh $h 'sudo systemctl daemon-reload'
    ssh $h 'sudo systemctl restart agv.service'
    ssh $h 'sudo systemctl reenable agv.service'
    if [[ $h != moro ]]
    then
        ssh $h 'sudo systemctl restart granier.service'
        ssh $h 'sudo systemctl reenable granier.service'
    fi
    ) &
done

wait
