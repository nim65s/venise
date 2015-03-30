from pprint import pprint

from .settings import hosts
from .sortie import Sortie


class SortiePrint(Sortie):
    def process(self):
        pprint(self.state)


if __name__ == '__main__':
    SortiePrint(host=hosts.ame).loop()
