#!/bin/bash

pssh -H cerf -H moro -H ame -H yuki 'cd venise; git pull'
pssh -H moro -H ame -H yuki 'sudo systemctl restart agv'
