from pprint import pprint

from .sortie import Sortie


class SortiePrint(Sortie):
    def process(self):
        pprint(self.state)
