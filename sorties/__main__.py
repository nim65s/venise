from .settings import hosts
from .sortie_ap import SortieAGVPrint as default

if __name__ == '__main__':
    default(host=hosts.yuki).loop()
