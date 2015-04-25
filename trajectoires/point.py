from argparse import ArgumentParser
from math import atan2, hypot

from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoirePoint(Trajectoire):
    def __init__(self, xi, yi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xi, self.yi = xi, yi

    def process_speed(self, x, y, a, hote, **kwargs):
        if x == y == a == 0:
            return {'v': 0, 'w': 0}
        xi, yi = 11, 11
        if hypot(xi - x, yi - y) < 0.2:
            self.fini = True
            return {'v': 0, 'w': 0}
        return {'v': 2, 'w': 0, 't': atan2(y - yi, x - xi) - a}

trajectoire_point_parser = ArgumentParser(parents=[trajectoire_parser], conflict_handler='resolve')
trajectoire_point_parser.add_argument('--xi', type=float, default=11, help="Abscisse du point cible")
trajectoire_point_parser.add_argument('--yi', type=float, default=11, help="Ordonnée du point cible")

if __name__ == '__main__':
    TrajectoirePoint(**vars(trajectoire_point_parser.parse_args())).run()
