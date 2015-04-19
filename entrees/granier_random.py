from random import random

from .granier import Granier, granier_parser


class GranierRandom(Granier):
    def process(self, value):
        return [round(min(self.maxi, max(self.mini, v + (random() - 0.5) / 10)), 4) for v in value]


if __name__ == '__main__':
    GranierRandom(**vars(granier_parser.parse_args())).run()
