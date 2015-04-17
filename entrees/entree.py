from argparse import ArgumentParser
from time import sleep

from ..settings import PERIODE
from ..vmq import Pusher, vmq_parser


class Entree(Pusher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period

    def loop(self):
        self.process(**self.data[self.hote])
        self.send()
        sleep(self.period)

    def process(self):
        raise NotImplementedError()

entree_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
entree_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données à l’hôte principal (0 pour un seul envoi)")
