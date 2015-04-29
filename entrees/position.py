from argparse import ArgumentParser
# TODO from datetime import datetime
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
        self.correction = [0, 0, 2.32, 0.781, 0.828]

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
            for data in self.conn.recv(4096).decode('UTF-16LE').split('C'):  # Merci VinDuv
                if not data or data.endswith('e'):
                    continue
                try:
                    data = data.split()
                    if len(data) != 6:
                        print('Pas prêt… %r' % data)
                        continue
                    arbre, x, y, a, jour, heure = data
                    arbre, x, y, a = int(arbre[-1]) + 1, float(x.replace(',', '.')), float(y.replace(',', '.')), float(a.replace(',', '.'))
                    # TODO last_seen = datetime.strptime('%s %s' % (jour, heure), '%d/%m/%Y %H:%M:%S')
                    self.data[arbre].update(x=x, y=y, a=round(a - self.correction[arbre], 3))
                except:
                    print('Pas prêt… %r' % data)
        except ConnectionResetError:
            print('Déconnecté…')
            self.connect()

position_parser = ArgumentParser(parents=[entree_parser], conflict_handler='resolve')
position_parser.set_defaults(hote=MAIN_HOST.name)

if __name__ == '__main__':
    EntreePosition(**vars(position_parser.parse_args())).run()
