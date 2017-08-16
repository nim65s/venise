from argparse import ArgumentParser
from random import uniform

from .destination import DestinationTrajectory, trajectory_destination_parser


class RandomDestination(DestinationTrajectory):
    """ in a square """
    def __init__(self, minx, miny, maxx, maxy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minx, self.miny, self.maxx, self.maxy = minx, miny, maxx, maxy

    def change_destination(self, host, **kwargs):
        self.data[host]['destination'] = (uniform(self.minx, self.maxx), uniform(self.miny, self.maxy))
        print('new destination:', self.data[host]['destination'])


random_destination_parser = ArgumentParser(parents=[trajectory_destination_parser], conflict_handler='resolve')
random_destination_parser.add_argument('--minx', type=float, default=-5)
random_destination_parser.add_argument('--miny', type=float, default=-5)
random_destination_parser.add_argument('--maxx', type=float, default=5)
random_destination_parser.add_argument('--maxy', type=float, default=5)
