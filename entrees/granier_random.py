from random import random

from .granier import Granier


class GranierRandom(Granier):
    def __init__(self, *args, **kwargs):
        super(GranierRandom, self).__init__(*args, **kwargs)
        # self.value = [2 * random() - 1 for s in self.value]
        self.value = [0 for _ in self.value]

    def process(self):
        return [min(1, max(-1, s + (random() - 0.5) / 1000)) for s in self.value]
