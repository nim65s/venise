from math import pi, cos, sin, copysign

from .points import trajectoire_points_parser, TrajectoirePoints
from .aller_retours import TrajectoireAllerRetours

from ..settings import N_SONDES, Hote, SMOOTH_SPEED, ALLER_RETOURS


class TrajectoireGranier(TrajectoireAllerRetours):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permutations = {h: range(N_SONDES) for h in self.hotes}

    def process_speed(self, hote, granier, gmi, gma, gm, x, y, a, v, w, t, **kwargs):
        self.check_distance(hote, x, y)
        if not granier or x == y == a == 0:
            return {'v': 0, 'w': 0}
        for i in range(N_SONDES):
            gmi[i] = min(granier[i], gmi[i])
            gma[i] = max(granier[i], gma[i])
            gm[i] = round((granier[i] - gmi[i]) / (gma[i] - gmi[i] if gma[i] != gmi[i] else 1), 5)
        # TODO: en cas de croisement, on permute
        # for i in range(N_SONDES):
        #     if gmi[i] == gmi[(i + 1) % N_SONDES]:
        #         tmp = self.permutations[hote][i]
        #         self.permutations[hote][i] = self.permutations[hote][(i + 1) % N_SONDES]
        #         self.permutations[hote][(i + 1) % N_SONDES] = tmp
        #         print(hote, self.permutations)
        t = self.go_to_point(hote, x, y, a)['t']
        # TODO: ce lissage devrait pouvoir se faire dans une classe à part
        vg = round(cos(2 * pi * gm[self.permutations[hote][0]]) / 2 + 0.5, 5)
        wg = round(gm[self.permutations[hote][2]] * 2 - 1, 5)
        tg = round((sin(2 * pi * gm[self.permutations[hote][1]]) * pi / 2 + t) % (2 * pi), 5)

        return {
                'vg': vg, 'wg': wg, 'tg': tg,
                'gmi': gmi, 'gma': gma, 'gm': gm,
                }


if __name__ == '__main__':
    TrajectoireGranier(**vars(trajectoire_points_parser.parse_args())).run()
