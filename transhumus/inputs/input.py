from argparse import ArgumentParser
from time import sleep

from ..settings import PERIOD
from ..vmq import Pusher, parser


class Input(Pusher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period

    def loop(self):
        self.iteration()
        self.send()
        if self.period:
            sleep(self.period)
        else:
            self.ended = True

    def iteration(self):
        self.process(**self.data[self.host])

    def process(self, **kwargs):
        pass


input_parser = ArgumentParser(parents=[parser], conflict_handler='resolve')
input_parser.add_argument('-T', '--period', type=float, default=PERIOD,
                          help="period for sending data (0: one shot)")
