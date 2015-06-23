from argparse import ArgumentParser
from datetime import datetime
from math import hypot
from os.path import expanduser, isfile

from numpy import array, where

from ..settings import PATHS, Hote
from .destination import TrajectoireDestination, trajectoire_destination_parser


class TrajectoirePoints(TrajectoireDestination):
    def __init__(self, s1, s2, s3, cp1, cp2, cp3, sens1, sens2, sens3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_truc('sens', sens1, sens2, sens3)
        self.set_choosen_path(cp1, cp2, cp3)
        self.set_state(s1, s2, s3)
        self.paths = self.get_paths()
        self.length = {}
        self.get_length()
        for h in self.hotes:
            cp, s, x, y = [self.data[h][t] for t in ['choosen_path', 'state', 'x', 'y']]
            try:
                self.data[h]['destination'] = self.paths[h][cp][s]
            except IndexError:
                self.find_nearest_destination(h, cp, x, y)

    def get_paths(self):
        return PATHS

    def get_length(self):
        for h in self.hotes:
            p = self.paths[h][self.data[h]['choosen_path']]
            self.length[h] = [hypot(p[i][0] - p[(i + 1) % len(p)][0], p[i][1] - p[(i + 1) % len(p)][1]) for i in range(len(p))]

    def find_nearest_destination(self, hote, choosen_path, x, y):
        path = self.paths[hote][choosen_path]
        dists = ((array(path) - array([x, y])) ** 2).sum(axis=1)
        state = int(where(dists == dists.min())[0][0])
        print(x, y, path[state])
        self.data[hote].update(state=state, destination=path[state])

    def process_speed(self, hote, destination, x, y, dest_next, dest_prev, path_next, path_prev, choosen_path, **kwargs):
        if path_next or path_prev:
            self.change_path(hote, choosen_path, path_next, path_prev, x, y)
        if self.distance(destination, x, y) < 1 or dest_next or dest_prev or path_next or path_prev:
            self.change_destination(**self.data[hote])
        self.check_sens()
        return self.go_to_point(**self.data[hote])

    def change_path(self, hote, choosen_path, path_next, path_prev, x, y):
        choosen_path += 1 if path_next else -1 if path_prev else 0
        choosen_path %= len(self.paths[hote])
        self.data[hote].update(choosen_path=choosen_path, path_next=False, path_prev=False)
        self.save_choosen_path(hote, choosen_path)
        self.find_nearest_destination(hote, choosen_path, x, y)

    def change_destination(self, hote, x, y, sens, dest_next, dest_prev, state, choosen_path, **kwargs):
        nouveau = (-1 if dest_prev else 1) * (-1 if sens else 1)
        state = (state + nouveau) % len(self.paths[hote][choosen_path])
        destination = self.paths[hote][choosen_path][state]
        print(datetime.now(), hote, state, destination)
        self.data[hote].update(destination=destination, state=state, dest_prev=False, dest_next=False)
        self.save_state(hote, state)

    def save_choosen_path(self, hote, choosen_path):
        with open(expanduser('~/.choosen_path_%s_%i' % (self.__class__.__name__, hote)), 'w') as f:
            print(choosen_path, file=f)

    def save_state(self, hote, state):
        with open(expanduser('~/.state_%s_%i' % (self.__class__.__name__, hote)), 'w') as f:
            print(state, file=f)

    def set_truc(self, truc, moro, ame, yuki):
        self.data[Hote.moro][truc] = moro
        self.data[Hote.ame][truc] = ame
        self.data[Hote.yuki][truc] = yuki

    def set_choosen_path(self, cp1, cp2, cp3):
        self.set_truc('choosen_path', cp1, cp2, cp3)
        for h in self.hotes:
            if self.data[h]['choosen_path'] == -1:
                filename = expanduser('~/.choosen_path_%s_%i' % (self.__class__.__name__, h))
                if isfile(filename):
                    with open(filename, 'r') as f:
                        self.data[h]['choosen_path'] = int(f.read().strip())
                else:
                    self.data[h]['choosen_path'] = 0
        print('choosen_path', [self.data[h]['choosen_path'] for h in self.hotes])

    def set_state(self, s1, s2, s3):
        self.set_truc('state', s1, s2, s3)
        for h in self.hotes:
            if self.data[h]['state'] == -1:
                filename = expanduser('~/.state_%s_%i' % (self.__class__.__name__, h))
                if isfile(filename):
                    with open(filename, 'r') as f:
                        self.data[h]['state'] = int(f.read().strip())
        print('state', [self.data[h]['state'] for h in self.hotes])

    def check_sens(self):
        if sum(self.data[Hote.moro]['nt']) < -50:
            self.data[Hote.moro]['sens'] = True
        elif sum(self.data[Hote.moro]['nt']) > 50:
            self.data[Hote.moro]['sens'] = False
        e2, e3 = [self.data[h]['state'] for h in [Hote.ame, Hote.yuki]]
        u2, u3 = [self.data[h]['is_up'] for h in [Hote.ame, Hote.yuki]]
        e = len(self.paths[Hote.ame][self.data[Hote.ame]['choosen_path']])
        if False and min(abs(e2 - e3), e - abs(e2 - e3)) < 10 and u2 and u3:
            self.ecarte_23(e, e2, e3, self.data[Hote.ame]['sens'], self.data[Hote.yuki]['sens'])

    def ecarte_23(self, e, e2, e3, s2, s3):
        if (not s2) and (e3 - e2 if e3 > e2 else e - e2 + e3) < 10:
            print('Ame est trop près de Yuki, et part donc dans le sens négatif')
            self.data[Hote.ame].update(sens=True, dest_next=True)
        elif s2 and (e2 - e3 if e2 > e3 else e - e3 + e2) < 10:
            print('Ame est trop près de Yuki, et part donc dans le sens positif')
            self.data[Hote.ame].update(sens=False, dest_next=True)
        if (not s3) and (e2 - e3 if e2 > e3 else e - e3 + e2) < 8:
            print('Yuki est trop près de Ame, et part donc dans le sens négatif')
            self.data[Hote.yuki].update(sens=True, dest_next=True)
        elif s3 and (e3 - e2 if e3 > e2 else e - e2 + e3) < 8:
            print('Yuki est trop près de Ame, et part donc dans le sens positif')
            self.data[Hote.yuki].update(sens=False, dest_next=True)


trajectoire_points_parser = ArgumentParser(parents=[trajectoire_destination_parser], conflict_handler='resolve')
trajectoire_points_parser.add_argument('--s1', type=int, default=-1)
trajectoire_points_parser.add_argument('--s2', type=int, default=-1)
trajectoire_points_parser.add_argument('--s3', type=int, default=-1)
trajectoire_points_parser.add_argument('--cp1', type=int, default=-1, choices=list(range(len(PATHS[Hote.moro]))) + [-1])
trajectoire_points_parser.add_argument('--cp2', type=int, default=-1, choices=list(range(len(PATHS[Hote.ame]))) + [-1])
trajectoire_points_parser.add_argument('--cp3', type=int, default=-1, choices=list(range(len(PATHS[Hote.yuki]))) + [-1])
trajectoire_points_parser.add_argument('--sens1', type=bool, default=bool((datetime.now()).day % 2))
trajectoire_points_parser.add_argument('--sens2', type=bool, default=not bool((datetime.now()).day % 2))
trajectoire_points_parser.add_argument('--sens3', type=bool, default=bool((datetime.now()).day % 2))

if __name__ == '__main__':
    TrajectoirePoints(**vars(trajectoire_points_parser.parse_args())).run()
