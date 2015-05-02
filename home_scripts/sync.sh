#!/bin/bash

echo git pull
pssh -H cerf -H moro -H ame -H yuki 'cd ~/venise; git pull'
echo vide le cache
pssh -H moro -H ame -H yuki "find ~/venise/ -name '*.pyc' -delete; find ~/venise/ -name __pycache__ -delete"
echo restart agv
pssh -H moro -H ame -H yuki 'sudo systemctl restart agv'
