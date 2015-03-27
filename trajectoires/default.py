from numpy import mean, median, var

from .settings import hosts
from .trajectoire import Trajectoire


class DefaultTrajectoire(Trajectoire):
    def process(self, host):
        sondes = self.data[host]['granier'] if 'granier' in self.data[host] else [0]
        return {
                'v': mean(sondes),
                'w': median(sondes),
                't': var(sondes),
                }

if __name__ == '__main__':
    DefaultTrajectoire().loop()
