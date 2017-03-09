from argparse import ArgumentParser
from time import sleep

from ..vmq import Pusher, Subscriber, subscriber_parser
from ..settings import PERIOD


class Processor(Subscriber, Pusher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period

    def loop(self):
        self.sub()
        self.send(self.process(**self.data[self.host]))
        if self.period:
            sleep(self.period)
        else:
            self.ended = True

    def send(self, data):
        self.printe(data)
        self.push.send_json([self.host, data])


processor_parser = ArgumentParser(parents=[subscriber_parser], conflict_handler='resolve')
processor_parser.add_argument('-T', '--period', type=float, default=PERIOD, help="period for processing data (0: one shot)")
