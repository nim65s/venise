from argparse import ArgumentParser
from random import random

from .probe import Probe, probe_parser


class GranierRandom(Probe):
    def process(self, value):
        return [round(min(self.maxi, max(self.mini, v + (random() - 0.5) / 10)), 4) for v in value]


granier_parser = ArgumentParser(parents=[probe_parser], conflict_handler='resolve')
granier_parser.set_defaults(name='granier', period=25, n_values=3, maxi=5, mini=0)

if __name__ == '__main__':
    GranierRandom(**vars(granier_parser.parse_args())).run()
