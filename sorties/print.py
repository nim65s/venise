from pprint import pprint

from .settings import hosts
from .sortie import Sortie


class Print(Sortie):
    def process(self):
        pprint(self.state)


if __name__ == '__main__':
    Print(host=hosts.ame).loop()
