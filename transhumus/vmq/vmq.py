from argparse import ArgumentParser
from pprint import pprint

from zmq import Context

from ..settings import MAIN_HOST, MAIN_HOSTS, Host


class VMQ(object):
    def __init__(self, main, host, verbosity, *args, **kwargs):
        self.main, self.host, self.verbosity = main, Host[host], verbosity
        self.hosts = [Host.ame]
        self.log(self.hosts)
        self.context = Context()
        self.data = {h: {} for h in self.hosts}
        self.ended = False

    def run(self):
        try:
            while not self.ended:
                self.loop()
        except:
            pass
        finally:
            self.end()
            print()

    def loop(self):
        # Abstract Class
        raise NotImplementedError

    def end(self):
        print('terminating…')

    def log(self, data=None):
        if data is None:
            data = self.data
        if self.verbosity > 1:
            pprint(data)
        elif self.verbosity > 0:
            print(data)


parser = ArgumentParser(conflict_handler='resolve')
parser.add_argument('-M', '--main', default=MAIN_HOST.name, choices=MAIN_HOSTS,
                    help="main host")
parser.add_argument('-H', '--host', default=Host.ame.name, choices=[h.name for h in Host],
                    help="source host")
parser.add_argument('-V', '--verbosity', action='count', default=0, help="set verbosity")
