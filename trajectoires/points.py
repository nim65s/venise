from argparse import ArgumentParser
from datetime import datetime
from os.path import expanduser, isfile

from ..settings import PATHS
from .destination import TrajectoireDestination, trajectoire_destination_parser


class TrajectoirePoints(TrajectoireDestination):
    def __init__(self, s1, s2, s3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_state(s1, s2, s3)
        self.paths = self.get_paths()
        for hote in self.hotes:
            self.destination[hote] = self.paths[hote][self.state[hote]]

    def get_paths(self):
        return PATHS

    def process_speed(self, x, y, a, w, hote, **kwargs):
        self.check_distance(hote, x, y)
        return self.go_to_point(hote, x, y, a)

    def check_distance(self, hote, x, y):
        if self.distance(hote, x, y) > 0.5:
            return
        self.state[hote] = (self.state[hote] + 1) % len(self.paths[hote])
        print(datetime.now(), hote, self.state[hote], self.paths[hote][self.state[hote]])
        self.destination[hote] = self.paths[hote][self.state[hote]]
        self.save_state(hote)

    def save_state(self, hote):
        with open(expanduser('~/.state_%s_%i' % (self.__class__.__name__, hote)), 'w') as f:
            print(self.state[hote], file=f)

    def set_state(self, s1, s2, s3):
        self.state = {2: s1, 3: s2, 4: s3}
        for i in [2, 3, 4]:
            if self.state[i] == -1:
                filename = expanduser('~/.state_%s_%i' % (self.__class__.__name__, i))
                if isfile(filename):
                    with open(filename, 'r') as f:
                        self.state[i] = int(f.read().strip())
        print(self.state)

trajectoire_points_parser = ArgumentParser(parents=[trajectoire_destination_parser], conflict_handler='resolve')
trajectoire_points_parser.add_argument('--s1', type=int, default=-1, choices=list(range(len(PATHS[2]))) + [-1])
trajectoire_points_parser.add_argument('--s2', type=int, default=-1, choices=list(range(len(PATHS[3]))) + [-1])
trajectoire_points_parser.add_argument('--s3', type=int, default=-1, choices=list(range(len(PATHS[4]))) + [-1])

if __name__ == '__main__':
    TrajectoirePoints(**vars(trajectoire_points_parser.parse_args())).run()
