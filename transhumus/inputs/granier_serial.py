from argparse import ArgumentParser
from datetime import datetime
from os.path import expanduser

from serial import Serial

from .probe import Probe, p_parser


class GranierSerial(Probe):
    def __init__(self, port, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = Serial('/dev/ttyUSB%i' % port, 38400)
        self.filename = expanduser(filename % self.host)

    def process(self, value):
        l = self.serial.readline().decode('ascii')
        l = l.replace('\x00', '').replace('\x04', '').split()
        try:
            datetime.strptime(' '.join(l[:2]), '%d-%m-%y %H:%M:%S')
        except:
            print('fail:', l)
            return []
        with open(self.filename, 'a') as f:
            print(';'.join(l[:5]), file=f)
        return [round(float(l[2 + s]), 5) for s in range(3)]

    def end(self):
        self.serial.close()


gs_parser = ArgumentParser(parents=[p_parser], conflict_handler='resolve')
gs_parser.add_argument('-p', '--port', type=int, default=0)
gs_parser.add_argument('-f', '--filename', default='~/granier_%i.log',
                       help="log filename")
gs_parser.set_defaults(period=30)

if __name__ == '__main__':
    GranierSerial(**vars(gs_parser.parse_args())).run()
