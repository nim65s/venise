from numpy import mean, median, var

from .settings import hosts
from .trajectoire import Trajectoire


class DefaultTrajectoire(Trajectoire):
    def process_speed(self, host):
        if 'granier' not in self.data[host]:
            return {}
        sondes = self.data[host]['granier']
        return {
                'v': mean(sondes),
                'w': median(sondes),
                't': var(sondes),
                }

if __name__ == '__main__':
    DefaultTrajectoire().loop()
