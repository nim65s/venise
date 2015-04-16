from datetime import datetime

from ..vmq.subscriber import subscriber_parser
from .sortie import Sortie


class SortieFile(Sortie):
    def process(self, **kwargs):
        s = '%s\t%r' % (datetime.now().strftime('%x %X'), self.data['granier'])
        print(s)
        with open('/home/nim/LAAS/sondes.txt', 'a') as f:
            f.write(s + '\n')


if __name__ == '__main__':
    SortieFile(**vars(subscriber_parser.parse_args())).run()
