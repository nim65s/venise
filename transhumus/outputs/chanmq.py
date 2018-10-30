import os
from argparse import ArgumentParser
from time import sleep

import requests

from ..settings import PERIOD
from ..vmq import Subscriber, parser


class ChanMQOutput(Subscriber):
    def __init__(self, hostname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hostname = hostname

    def loop(self):
        self.sub()
        requests.post(f'http://{self.hostname}/in/{self.host}', data=self.data[self.host])
        sleep(PERIOD)


DOMAIN_NAME = os.environ.get(f'DOMAIN_NAME', 'localhost')
chan_parser = ArgumentParser(parents=[parser], conflict_handler='resolve')
chan_parser.add_argument('--hostname', default=f'chanmq.{DOMAIN_NAME}')

if __name__ == '__main__':
    ChanMQOutput(**vars(chan_parser.parse_args())).run()
