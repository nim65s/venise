from argparse import ArgumentParser
from datetime import datetime
from json import dumps
from time import sleep

from ..settings import MAIN_HOST
from ..vmq import vmq_parser
from .sortie import Sortie


class SortieFile(Sortie):
    def __init__(self, filename, periode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename, self.periode = filename, periode

    def process(self, **kwargs):
        with open(self.filename, 'a') as f:
            f.write('%s\t%r\n' % (datetime.now().strftime('%y/%m/%d %H:%M:%S'), dumps(self.data)))
        sleep(self.periode)


sortie_file_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
sortie_file_parser.set_defaults(hote=MAIN_HOST.name)
sortie_file_parser.add_argument('-f', '--filename', default='logs/all.log')
sortie_file_parser.add_argument('-T', '--periode', type=float, default=1)

if __name__ == '__main__':
    SortieFile(**vars(sortie_file_parser.parse_args())).run()
