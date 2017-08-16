from argparse import ArgumentParser
from datetime import datetime
from time import sleep

from ..vmq import Pusher, vmq_parser
from ..settings import PERIODE


class TestGranier(Pusher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period

    def loop(self):
        self.data[self.hote].update(**self.process(**self.data[self.hote]))
        self.send()
        sleep(self.period)

    def process(self, **kwargs):
        return {'granier': datetime.now().strftime('%f')}


entree_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
entree_parser.add_argument('-T', '--period', type=float, default=PERIODE,
                           help="période d’envoie des données à l’hôte principal (0 pour un seul envoi)")

if __name__ == '__main__':
    TestGranier(**vars(entree_parser.parse_args())).run()
