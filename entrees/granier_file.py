from datetime import datetime
from time import sleep

from .granier import Granier, granier_parser


class GranierFile(Granier):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dates, self.sondes = [], [[], [], []]
        with open(filename, 'r') as f:
            for line in f.readlines():
                l = line.split()
                try:
                    d = datetime.strptime(' '.join(l[:2]), '%d-%m-%y %H:%M:%S')
                except:
                    continue
                self.dates.append(d)
                for s in range(3):
                    self.sondes[s].append(l[2 + s])

    def loop(self):
        d = self.dates[0]
        i = 0
        while d < self.dates[-1]:
            if d > self.dates[i]:
                pass  # TODO
