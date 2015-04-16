from argparse import ArgumentParser
from datetime import datetime

from serial import Serial

from .granier import Granier, granier_parser


class GranierSerie(Granier):
    def __init__(self, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = Serial('/dev/ttyUSB%i' % port, 38400)

    def process(self, value):
        l = self.serial.readline().decode('ascii').replace('\x00', '').replace('\x04', '').split()
        try:
            datetime.strptime(' '.join(l[:2]), '%d-%m-%y %H:%M:%S')
        except:
            print('fail:', l)
            return {}
        ret = [float(l[2 + s]) for s in range(3)]
        print(ret)
        return ret

    def end(self):
        self.serial.close()

granier_serie_parser = ArgumentParser(parents=[granier_parser], conflict_handler='resolve')
granier_serie_parser.add_argument('-p', '--port', type=int, default=0)
granier_serie_parser.set_defaults(period=30, maxi=1)

if __name__ == '__main__':
    GranierSerie(**vars(granier_serie_parser.parse_args())).loop()
