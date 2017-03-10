from datetime import datetime
from math import sin

from .points import TrajectoirePoints, trajectoire_points_parser


class TrajectoireGranier(TrajectoirePoints):
    def get_w(self, gm, **kwargs):
        return round(gm[1] * 2 - 1, 5)
        #return .5

    def get_v(self, gm, **kwargs):
        return round(gm[2] * 2 - 1, 5)
        #return 1

        #return round((-1) ** datetime.now().day * (-1) ** hote * sin(gm[0]) / 2, 5) if rotation else 0
        # vg = round(cos(2 * pi * gm[self.permutations[hote][0]]) / 2 + 0.5, 5)
        # tg = round((sin(2 * pi * gm[self.permutations[hote][1]]) * pi / 2 + t) % (2 * pi), 5)


if __name__ == '__main__':
    TrajectoireGranier(**vars(trajectoire_points_parser.parse_args())).run()
