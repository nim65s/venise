from argparse import ArgumentParser
from datetime import datetime
from socket import socket  # , AF_INET, SOCK_STREAM

from ..settings import Hote, MAIN_HOST, PORT_UBISENS
from .entree import Entree, entree_parser


class EntreePosition(Entree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {h: {
            'x': 0, 'y': 0, 'a': 0,  # Position
            # TODO 'last_seen': None,
            } for h in Hote}
        self.socket = socket()
        self.connect()

    def connect(self):
        self.socket.close()
        self.socket = socket()
        self.socket.bind(('', PORT_UBISENS))
        self.socket.listen(1)
        print('Attente d’une connexion…')
        self.conn, self.addr = self.socket.accept()
        print('Connecté à %s:%i' % self.addr)

    def process(self, **kwargs):
        try:
            data = self.conn.recv(1024).decode('UTF-16LE').split()  # Merci VinDuv
            if len(data) != 6:
                print('Pas prêt… %r' % data)
                return
            arbre, x, y, a, jour, heure = data
            # TODO last_seen = datetime.strptime('%s %s' % (jour, heure), '%d/%m/%Y %H:%M:%S')
            self.data[int(arbre[-1]) + 1].update(x=float(x), y=float(y), a=round(float(a) - 0.828, 3))  # TODO
        except ConnectionResetError:
            print('Déconnecté…')
            self.connect()

position_parser = ArgumentParser(parents=[entree_parser], conflict_handler='resolve')
position_parser.set_defaults(hote=MAIN_HOST.name)

if __name__ == '__main__':
    EntreePosition(**vars(position_parser.parse_args())).run()
