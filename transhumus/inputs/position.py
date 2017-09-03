from socket import socket

from ..settings import PORT_UBISENS, Host
from .input import Input, input_parser


class PositionInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {h: {
            'x': 0, 'y': 0, 'a': 0,  # Position
            } for h in Host}
        self.socket = socket()
        self.connect()
        self.correction = [0, 0, 2.52, 0.781, 0.828]

    def connect(self):
        self.socket.close()
        self.socket = socket()
        self.socket.bind(('', PORT_UBISENS))
        self.socket.listen(1)
        print('Waiting for a connection from ubisens…')
        self.conn, self.addr = self.socket.accept()
        print('Connection with ubisens established at %s:%i' % self.addr)

    def process(self, **kwargs):
        try:
            for data in self.conn.recv(4096).decode('UTF-16LE').split('C'):
                if not data or data.endswith('e'):
                    continue
                try:
                    data = data.split()
                    if len(data) != 6:
                        print('Not ready … %r' % data)
                        continue
                    tree, x, y, a, day, hour = data
                    tree, x, y, a = [int(tree[-1]) + 1] + [float(i.replace(',', '.')) for i in (x, y, a)]
                    self.data[tree].update(x=x, y=y, a=round(a - self.correction[tree], 3))
                except:
                    print('Not ready… %r' % data)
        except ConnectionResetError:
            print('Disconnected…')
            self.connect()


if __name__ == '__main__':
    PositionInput(**vars(input_parser.parse_args())).run()
