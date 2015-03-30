from .settings import hosts
from .sortie_print import SortiePrint as default

if __name__ == '__main__':
    default(host=hosts.ame).loop()
