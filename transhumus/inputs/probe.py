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
            raise ValueError(f'len({value}) != {self.n_values}')
        for i, v in enumerate(value):
            if not self.mini <= v <= self.maxi:
                raise ValueError(f'{v} not beetwen {self.mini} and {self.maxi}')
        self.data[self.host][self.name] = value


p_parser = ArgumentParser(parents=[input_parser], conflict_handler='resolve')
p_parser.add_argument('-n', '--name', choices=['granier', 'sick', 'brightness'])
p_parser.add_argument('-m', '--mini', type=float, default=-1)
p_parser.add_argument('-M', '--maxi', type=float, default=1)
p_parser.add_argument('-N', '--n_values', type=int, default=1)
