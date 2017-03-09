from argparse import ArgumentParser
from math import tau

from .input import Input, input_parser

DEFAULT = 9


class ShellInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for var in ['v', 'w', 't', 'vg', 'wg', 'tg']:
            if kwargs[var] != DEFAULT:
                self.data[self.host][var] = kwargs[var]
        if kwargs['stop']:
            self.data[self.host]['stop'] = kwargs['stop']


shell_input_parser = ArgumentParser(parents=[input_parser], conflict_handler='resolve')
shell_input_parser.add_argument('-v', type=float, default=DEFAULT, help="linear speed")
shell_input_parser.add_argument('-w', type=float, default=DEFAULT, help="angular speed")
shell_input_parser.add_argument('-t', type=float, default=DEFAULT, help="direction")
shell_input_parser.add_argument('--vg', type=float, default=DEFAULT, help="goal linear speed")
shell_input_parser.add_argument('--wg', type=float, default=DEFAULT, help="goal angular speed")
shell_input_parser.add_argument('--tg', type=float, default=DEFAULT, help="goal direction")
shell_input_parser.add_argument('-s', '--stop', action='store_true', help="stop the AGV")
shell_input_parser.set_defaults(period=0)

if __name__ == '__main__':
    ShellInput(**vars(shell_input_parser.parse_args())).run()
