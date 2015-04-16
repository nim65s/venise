from argparse import ArgumentParser
from time import sleep

from .entree import Entree, entree_parser


class Sonde(Entree):
    def __init__(self, nom, mini, maxi, n_values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nom, self.mini, self.maxi, self.n_values = nom, mini, maxi, n_values
        self.data[self.hote][nom] = [(maxi + mini) / 2] * n_values

    def loop(self):
        self.send(self.check_value(self.process(self.data[self.hote][self.nom])))
        sleep(self.period)

    def check_value(self, value):
        if len(value) != self.n_values:
            raise ValueError('%s sur %s: len(%r) != %i' % (self.nom, self.hote.name, value, self.n_values))
        for i, v in enumerate(value):
            if not self.mini <= v <= self.maxi:
                raise ValueError('%s.%i sur %s: %f pas entre %f et %f' % (self.nom, i, self.hote.name, v, self.mini, self.maxi))
        self.data[self.hote][self.nom] = value
        return self.data[self.hote]

sonde_parser = ArgumentParser(parents=[entree_parser], conflict_handler='resolve')
sonde_parser.add_argument('-n', '--nom', choices=['granier', 'sick', 'luminosite'])
sonde_parser.add_argument('-m', '--mini', type=float, default=-1)
sonde_parser.add_argument('-M', '--maxi', type=float, default=1)
sonde_parser.add_argument('-N', '--n_values', type=int, default=1)
