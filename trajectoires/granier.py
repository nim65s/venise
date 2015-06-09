from math import cos, pi

from .points import trajectoire_points_parser, TrajectoirePoints


class TrajectoireGranier(TrajectoirePoints):
    def get_w(self, gm, hote, **kwargs):
        return round(- (-1) ** hote * cos(2 * pi * gm[0]) / 2, 5)
        # vg = round(cos(2 * pi * gm[self.permutations[hote][0]]) / 2 + 0.5, 5)
        # wg = round(gm[self.permutations[hote][2]] * 2 - 1, 5)
        # tg = round((sin(2 * pi * gm[self.permutations[hote][1]]) * pi / 2 + t) % (2 * pi), 5)


if __name__ == '__main__':
    TrajectoireGranier(**vars(trajectoire_points_parser.parse_args())).run()
