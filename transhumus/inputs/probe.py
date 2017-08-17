from argparse import ArgumentParser

from .input import Input, input_parser


class Probe(Input):
    def __init__(self, name, mini, maxi, n_values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name, self.mini, self.maxi, self.n_values = name, mini, maxi, n_values
        self.data[self.host][name] = [(maxi + mini) / 2] * n_values

    def iteration(self):
        self.check_value(self.process(self.data[self.host][self.name]))

    def check_value(self, value):
        if len(value) != self.n_values:
            raise ValueError('%s sur %s: len(%r) != %i' % (self.name, self.host.name, value, self.n_values))
        for i, v in enumerate(value):
            if not self.mini <= v <= self.maxi:
                raise ValueError('%s.%i on %s: %f not beetwen %f and %f' %
                                 (self.name, i, self.host.name, v, self.mini, self.maxi))
        self.data[self.host][self.name] = value


probe_parser = ArgumentParser(parents=[input_parser], conflict_handler='resolve')
probe_parser.add_argument('-n', '--name', choices=['granier', 'sick', 'brightness'])
probe_parser.add_argument('-m', '--mini', type=float, default=-1)
probe_parser.add_argument('-M', '--maxi', type=float, default=1)
probe_parser.add_argument('-N', '--n_values', type=int, default=1)
