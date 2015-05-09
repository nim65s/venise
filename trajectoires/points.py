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
            self.data[hote]['destination'] = self.paths[hote][self.data[hote]['state']]

    def get_paths(self):
        return PATHS

    def process_speed(self, hote, **kwargs):
        self.check_distance(**self.data[hote])
        return self.go_to_point(**self.data[hote])

    def check_distance(self, hote, destination, x, y, sens, dest_next, dest_prev, **kwargs):
        if self.distance(destination, x, y) > 1 and not dest_next and not dest_prev:
            return
        self.change_destination(**self.data[hote])

    def change_destination(self, hote, x, y, sens, dest_next, dest_prev, state, **kwargs):
        nouveau = (-1 if dest_prev else 1)
        if sens:
            nouveau *= -1
        state = (state + nouveau) % len(self.paths[hote])
        destination = self.paths[hote][state]
        print(datetime.now(), hote, state, destination)
        self.data[hote].update(destination=destination, state=state, dest_prev=False, dest_next=False)
        self.save_state(hote)

    def save_state(self, hote):
        with open(expanduser('~/.state_%s_%i' % (self.__class__.__name__, hote)), 'w') as f:
            print(self.data[hote]['state'], file=f)

    def set_state(self, s1, s2, s3):
        self.data[2]['state'] = s1
        self.data[3]['state'] = s2
        self.data[4]['state'] = s3
        for i in [2, 3, 4]:
            if self.data[i]['state'] == -1:
                filename = expanduser('~/.state_%s_%i' % (self.__class__.__name__, i))
                if isfile(filename):
                    with open(filename, 'r') as f:
                        self.data[i]['state'] = int(f.read().strip())
        print([self.data[i]['state'] for i in [2, 3, 4]])

trajectoire_points_parser = ArgumentParser(parents=[trajectoire_destination_parser], conflict_handler='resolve')
trajectoire_points_parser.add_argument('--s1', type=int, default=-1, choices=list(range(len(PATHS[2]))) + [-1])
trajectoire_points_parser.add_argument('--s2', type=int, default=-1, choices=list(range(len(PATHS[3]))) + [-1])
trajectoire_points_parser.add_argument('--s3', type=int, default=-1, choices=list(range(len(PATHS[4]))) + [-1])

if __name__ == '__main__':
    TrajectoirePoints(**vars(trajectoire_points_parser.parse_args())).run()
