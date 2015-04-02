from .settings import hosts
from .trajectoire import Trajectoire

ligne = {'v': 1, 'w': 0, 't': 0}
z = {'v': 0, 'w': 1, 't': 0}
manuel = {}


class TrajectoireManuelle(Trajectoire):
    def process_speed(self, host, v, w, t, **kwargs):
        if host != hosts.yuki:
            return {}
        return manuel

if __name__ == '__main__':
    TrajectoireManuelle().loop()
