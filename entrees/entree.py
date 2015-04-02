from argparse import ArgumentParser
from time import sleep

from .pusher import Pusher, pusher_parser
from .settings import PERIODE


class Entree(Pusher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.data = {}

    def loop(self):
        while self.period:
            self.send(self.process(**self.data))
            sleep(self.period)

    def process(self):
        raise NotImplementedError()

entree_parser = ArgumentParser(parents=[pusher_parser])
entree_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données à l’hôte principal")
