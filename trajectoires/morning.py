from ..settings import MORNING
from .destination import TrajectoireDestination, trajectoire_destination_parser


class TrajectoireMorning(TrajectoireDestination):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for hote in self.hotes:
            self.destination[hote] = MORNING[hote]
        self.arrive = {h: False for h in self.hotes}

    def process_speed(self, x, y, a, hote, **kwargs):
        if self.arrive[hote] or self.distance(hote, x, y) < 0.5:
            self.arrive[hote] = True
            if all([self.arrive[h] for h in self.hotes]):
                self.fini = True
            return {'stop': True}
        return self.go_to_point(hote, x, y, a)


if __name__ == '__main__':
    TrajectoireMorning(**vars(trajectoire_destination_parser.parse_args())).run()
