from math import atan2, copysign, hypot

from ..settings import BERCAIL
from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireBercail(Trajectoire):
    def process_speed(self, x, y, a, hote, **kwargs):
        xi, yi = BERCAIL[hote]
        if hypot(xi - x, yi - y) < 0.3:
            return {'v': 0, 'w': 0, 'stop': True}
        return {
                'v': 1,
                't': atan2(y - yi, x - xi) - a,
                'w': 0,
                }

if __name__ == '__main__':
    TrajectoireBercail(**vars(trajectoire_parser.parse_args())).run()
