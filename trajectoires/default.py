from numpy import mean, median, var

from .trajectoire import Trajectoire


class TrajectoireDefault(Trajectoire):
    def process_speed(self, host):
        if 'granier' not in self.data[host]:
            return {}
        sondes = self.data[host]['granier']
        return {
                'v': mean(sondes),
                'w': median(sondes),
                't': var(sondes),
                }
