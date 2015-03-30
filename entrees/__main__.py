#from .granier_random import GranierRandom as default
from .manuelle import EntreeManuelle as default
from .settings import hosts

if __name__ == '__main__':
    default(host=hosts.yuki).loop()
