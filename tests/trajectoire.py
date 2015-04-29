from argparse import ArgumentParser
from zmq import PUSH
from datetime import datetime
from time import sleep

from ..settings import PORT_PUSH, PERIODE
from ..vmq import Puller, Publisher, vmq_parser


class TestTrajectoire(Puller, Publisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(wait=False, *args, **kwargs)
        self.period = period
        self.data = {h: {
            'granier': None,
            'agv': None,
            'web': None,
            } for h in self.hotes}
        self.data['timestamp'] = datetime.now().timestamp()
        self.push = {h: self.context.socket(PUSH) for h in self.hotes}
        for h in self.hotes:
            self.push[h].connect('tcp://%s:%i' % (h.name, PORT_PUSH))

    def send(self):
        self.data['timestamp'] = datetime.now().timestamp()
        self.pub()
        for h in self.hotes:
            self.push[h].send_json([h, self.data[h]])

    def loop(self):
        self.pull()
        self.send()
        sleep(self.period)

trajectoire_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
trajectoire_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données aux sorties")

if __name__ == '__main__':
    TestTrajectoire(**vars(trajectoire_parser.parse_args())).run()
