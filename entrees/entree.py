from argparse import ArgumentParser
from time import sleep

from ..settings import PERIODE
from ..vmq.pusher import Pusher, pusher_parser


class Entree(Pusher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.data = {}

    def loop(self):
        if self.period == 0:
            self.send(self.process(**self.data))
            return
        while True:
            try:
                self.send(self.process(**self.data))
                sleep(self.period)
            except KeyboardInterrupt:
                print()
                self.end()
                break

    def process(self):
        raise NotImplementedError()

    def end(self):
        pass

entree_parser = ArgumentParser(parents=[pusher_parser], conflict_handler='resolve')
entree_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données à l’hôte principal (0 pour un seul envoi)")
