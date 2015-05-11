from argparse import ArgumentParser
from math import hypot
from datetime import datetime
from os.path import expanduser, isfile

from ..settings import PATHS, Hote
from .destination import TrajectoireDestination, trajectoire_destination_parser


class TrajectoirePoints(TrajectoireDestination):
    def __init__(self, s1, s2, s3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_state(s1, s2, s3)
        self.paths = self.get_paths()
        self.length = {}
        self.get_length()
        for hote in self.hotes:
            self.data[hote]['destination'] = self.paths[hote][self.data[hote]['state']]

    def get_paths(self):
        return PATHS

    def get_length(self):
        for h in self.hotes:
            p = self.paths[h]
            self.length[h] = [hypot(p[i][0] - p[(i + 1) % len(p)][0], p[i][1] - p[(i + 1) % len(p)][1]) for i in range(len(p))]

    def process_speed(self, hote, **kwargs):
        self.check_distance(**self.data[hote])
        return self.go_to_point(**self.data[hote])

    def check_distance(self, hote, destination, x, y, sens, dest_next, dest_prev, **kwargs):
        if self.distance(destination, x, y) > 1 and not dest_next and not dest_prev:
            return
        self.change_destination(**self.data[hote])

    def change_destination(self, hote, x, y, sens, dest_next, dest_prev, state, **kwargs):
        nouveau = (-1 if dest_prev else 1) * (-1 if sens else 1)
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

    def update(self):
        for hote in self.hotes:
            self.data[hote].update(avancement=self.avancement(**self.data[hote]))
        self.check_sens()
        super().update()

    def check_sens(self):
        if sum(self.data[Hote.moro]['nt']) < -50:
            print('Moro a trop tourné dans le sens direct, on passe à l’indirect')
            self.data[Hote.moro]['sens'] = True
        elif sum(self.data[Hote.moro]['nt']) > 50:
            print('Moro a trop tourné dans le sens indirect, on passe au direct')
            self.data[Hote.moro]['sens'] = False
        if self.distance_23() < 10:
            print('Moins de 10m entre ame et yuki')
            self.ecarte_23()

    def distance_23(self):
        a2, a3 = self.avancement(**self.data[Hote.ame]), self.avancement(**self.data[Hote.yuki])
        return min(abs(a2 - a3), sum(self.length[Hote.ame]) - abs(a2 - a3))

    def avancement(self, state, destination, x, y, hote, **kwargs):
        return sum(self.length[hote][:state] if state > 0 else self.length[hote]) - self.distance(destination, x, y)

    def ecarte_23(self):
        a2, a3 = self.avancement(**self.data[Hote.ame]), self.avancement(**self.data[Hote.yuki])
        print('avancement d’ame et yuki: %.2f & %.2f' % (a2, a3))
        sens = (True, False) if abs(a2 - a3) < sum(self.length[Hote.ame]) - abs(a2 - a3) else (False, True)
        print('nouveaux sens: %s & %s' % sens)
        self.data[Hote.ame]['sens'], self.data[Hote.yuki]['sens'] = sens


trajectoire_points_parser = ArgumentParser(parents=[trajectoire_destination_parser], conflict_handler='resolve')
trajectoire_points_parser.add_argument('--s1', type=int, default=-1, choices=list(range(len(PATHS[2]))) + [-1])
trajectoire_points_parser.add_argument('--s2', type=int, default=-1, choices=list(range(len(PATHS[3]))) + [-1])
trajectoire_points_parser.add_argument('--s3', type=int, default=-1, choices=list(range(len(PATHS[4]))) + [-1])

if __name__ == '__main__':
    TrajectoirePoints(**vars(trajectoire_points_parser.parse_args())).run()
