from argparse import ArgumentParser
from math import atan2, hypot, tau

from ..settings import Host
from .base_trajectory import t_parser
from .trajectory import Trajectory


class DestinationTrajectory(Trajectory):
    def __init__(self, v, w, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wi = {Host.ame: w}
        self.vi = {Host.ame: v}

    def process_speed(self, host, destination, x, y, **kwargs):
        if self.distance(destination, x, y) < 1:
            self.change_destination(**self.data[host])
        return self.go_to_point(**self.data[host])

    def distance(self, destination, x, y):
        xi, yi = destination
        return hypot(xi - x, yi - y)

    def go_to_point(self, host, destination, x, y, a, **kwargs):
        xi, yi = destination
        return {
            'vg': self.get_v(**self.data[host]),
            'wg': self.get_w(**self.data[host]),
            'tg': round((atan2(y - yi, x - xi) - a) % tau, 5),
        }

    def get_v(self, host, **kwargs):
        return self.vi[host]

    def get_w(self, host, **kwargs):
        return self.wi[host]

    def change_destination(self, **kwargs):
        raise NotImplementedError


t_destination_parser = ArgumentParser(parents=[t_parser], conflict_handler='resolve')
t_destination_parser.add_argument('--w', type=float, default=0)
t_destination_parser.add_argument('--v', type=float, default=1)
