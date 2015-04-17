from argparse import ArgumentParser
from pprint import pprint

from zmq import Context

from ..settings import CURRENT_HOST, Hote


class VMQ(object):
    def __init__(self, hote, verbosite, *args, **kwargs):
        self.hote, self.verbosite = Hote[hote], verbosite
        self.hotes = [self.hote] if self.hote > 1 else [h for h in Hote]
        if verbosite > 0:
            print(self.hotes)
        self.context = Context()
        self.data = {h: {} for h in self.hotes}

    def run(self):
        while True:
            try:
                self.loop()
            except KeyboardInterrupt:
                self.end()
                print()
                break

    def loop(self):
        raise NotImplementedError

    def end(self):
        print('terminating…')

    def print(self, data=None):
        if data is None:
            data = self.data
        if self.verbosite > 1:
            pprint(data)
        elif self.verbosite > 0:
            print(data)
        pass

vmq_parser = ArgumentParser(conflict_handler='resolve')
vmq_parser.add_argument('-H', '--hote', help="hôte source", default=CURRENT_HOST.name, choices=[h.name for h in Hote])
vmq_parser.add_argument('-V', '--verbosite', help="augmente la verbosité", action='count', default=0)
