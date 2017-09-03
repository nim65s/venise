from argparse import ArgumentParser
from time import sleep

from ..settings import DATA, PERIOD
from ..vmq import Publisher, Puller, parser


class BaseTrajectory(Puller, Publisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(wait=False, *args, **kwargs)
        self.period = period
        self.data = {h: DATA.copy() for h in self.hosts}
        for h in self.hosts:
            self.data[h]['host'] = h
        self.data['trajectory'] = self.__class__.__name__

    def send(self):
        self.pub()

    def loop(self):
        self.pull()
        self.update()
        self.send()
        sleep(self.period)

    def end(self):
        return

    def update(self):
        for host in self.hosts:
            self.data[host].update(**self.inside(**self.data[host]))
            self.data[host].update(**self.process_speed(**self.data[host]))
            self.data[host].update(**self.smooth_speed(**self.data[host]))
            self.data[host].update(**self.process_turrets(**self.data[host]))

    def process_speed(self, **kwargs):
        raise NotImplementedError


t_parser = ArgumentParser(parents=[parser], conflict_handler='resolve')
t_parser.add_argument('-T', '--period', type=float, default=PERIOD,
                      help="main loop period")
