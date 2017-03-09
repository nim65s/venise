from argparse import ArgumentParser
from datetime import datetime
from math import atan2, hypot, pi, sin

from ..settings import Host
from .trajectory import Trajectory, trajectory_parser


class DestinationTrajectory(Trajectory):
    def __init__(self, v, w, vw, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wi = {Host.ame: w}
        self.vi = {Host.ame: v}
        self.vw = vw

    def distance(self, destination, x, y):
        xi, yi = destination
        return hypot(xi - x, yi - y)

    def go_to_point(self, host, destination, x, y, a, **kwargs):
        xi, yi = destination
        return {
                'vg': self.get_v(**self.data[host]),
                'wg': self.get_w(**self.data[host]),
                'tg': round((atan2(y - yi, x - xi) - a) % (2 * pi), 5),
                }

    def get_v(self, host, **kwargs):
        return self.vi[host]

    def get_w(self, host, **kwargs):
        m = datetime.now().minute + datetime.now().second / 60
        return round(sin(m / 6) / self.vw, 5)


trajectory_destination_parser = ArgumentParser(parents=[trajectory_parser], conflict_handler='resolve')
trajectory_destination_parser.add_argument('--w', type=float, default=0)
trajectory_destination_parser.add_argument('--v', type=float, default=1)
trajectory_destination_parser.add_argument('--vw', type=float, default=2, help='ratio v / w')
