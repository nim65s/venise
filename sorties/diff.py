from time import sleep

from ..settings import PERIODE
from ..vmq import Subscriber, subscriber_parser


class Diff(Subscriber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub()
        self._data = {h: {} for h in self.hotes}

    def loop(self):
        self.sub()
        for h in self.hotes:
            for k in self.data[h]:
                if k not in self._data[h] or self._data[h][k] != self.data[h][k]:
                    self._data[h][k] = self.data[h][k]
                    self.diff(h, k, self._data[h][k])
        sleep(PERIODE)

    def diff(self, hote, key, data):
        print(hote, '\t', key, '\t', data)


if __name__ == '__main__':
    Diff(**vars(subscriber_parser.parse_args())).run()
