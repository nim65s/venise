#!/bin/bash

pssh -H cerf -H moro -H ame -H yuki 'cd ~/venise; git pull'
pssh -H moro -H ame -H yuki "find ~/venise/ -name '*.pyc' -delete; find ~/venise/ -name __pycache__ -delete"
pssh -H moro -H ame -H yuki 'sudo systemctl restart agv'
