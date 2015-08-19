from itertools import product

from numpy import array

from ..settings import BORDS, GRID_COEF
from ..utils.stay_in_poly import stay_in_poly
from .destination import trajectoire_destination_parser as parser
from .partout import TrajectoirePartout


class TrajectoireAvoid(TrajectoirePartout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.etoile = {}
        for h in self.hotes:
            g = self.grid[h].copy()
            b = abs(array(BORDS[h])) * GRID_COEF
            for i, j in product(*[range(int(x)) for x in self.grid_size[h]]):
                if g[i, j] != -1:
                    data = [stay_in_poly((i, j), dest, b, marge=0, strict=False) for dest in b]
                    print(data)
                    g[i, j] = int(all(data))
            self.etoile[h] = g


if __name__ == '__main__':
    TrajectoireAvoid(**vars(parser.parse_args())).run()
