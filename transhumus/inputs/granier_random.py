from argparse import ArgumentParser
from random import random

from .probe import Probe, p_parser


class GranierRandom(Probe):
    def process(self, value, **kwargs):
        return [round(min(self.maxi, max(self.mini, v + (random() - .5) / 10)), 4)
                for v in value]


gr_parser = ArgumentParser(parents=[p_parser], conflict_handler='resolve')
gr_parser.set_defaults(name='granier', period=25, n_values=3, maxi=5, mini=0)

if __name__ == '__main__':
    GranierRandom(**vars(gr_parser.parse_args())).run()
