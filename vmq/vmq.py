from argparse import ArgumentParser

from zmq import Context

from ..settings import CURRENT_HOST, Hote


class VMQ(object):
    def __init__(self, hote, verbosite, *args, **kwargs):
        self.hote, self.verbosite = Hote[hote], verbosite
        self.context = Context()
        self.data = {h: {
            'stop': False,
            'hote': h,
            'x': 0, 'y': 0, 'a': 0,  # Position
            'v': 0, 'w': 0, 't': 0,  # Vitesse
            't1': 0, 'v1': 0, 't2': 0, 'v2': 0, 't3': 0, 'v3': 0,  # Tourelles
            'granier': [], 'sick': [], 'luminosite': [],  # Sondes
            } for h in Hote}

    def run(self):
        while True:
            try:
                self.loop()
            except KeyboardInterrupt:
                self.end()
                print()
                break

    def end(self):
        print('terminating…')

    def print(self, data):
        #if self.verbosite > 1:
            #pprint(data)
        #elif self.verbosite > 0:
            #print(data)
        pass

vmq_parser = ArgumentParser(conflict_handler='resolve')
vmq_parser.add_argument('-H', '--hote', help="hôte source", default=CURRENT_HOST.name, choices=[h.name for h in Hote])
vmq_parser.add_argument('-V', '--verbosite', help="augmente la verbosité", action='count', default=0)
