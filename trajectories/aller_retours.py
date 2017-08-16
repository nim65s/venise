from .points import trajectoire_points_parser, TrajectoirePoints
from ..settings import ALLER_RETOURS


class TrajectoireAllerRetours(TrajectoirePoints):
    def get_paths(self):
        return ALLER_RETOURS


if __name__ == '__main__':
    TrajectoireAllerRetours(**vars(trajectoire_points_parser.parse_args())).run()
