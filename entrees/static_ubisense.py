from argparse import ArgumentParser

from ..settings import Hote, MAIN_HOST, PORT_UBISENS
from .entree import Entree, entree_parser


class EntreePosition(Entree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {
                Hote.moro: {'x': -7, 'y': 12, 'a': 0},
                Hote.ame: {'x': 8, 'y': 8, 'a': 0},
                Hote.yuki: {'x': 24, 'y': 9, 'a': 0},
                Hote.cerf: {},
                Hote.nausicaa: {},
                }

    def process(self, **kwargs):
        pass

position_parser = ArgumentParser(parents=[entree_parser], conflict_handler='resolve')
position_parser.set_defaults(hote=MAIN_HOST.name, period=10)

if __name__ == '__main__':
    EntreePosition(**vars(position_parser.parse_args())).run()
