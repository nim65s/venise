from argparse import ArgumentParser

from .sonde import Sonde, sonde_parser


class Granier(Sonde):
    pass

granier_parser = ArgumentParser(parents=[sonde_parser], conflict_handler='resolve')
granier_parser.set_defaults(nom='granier', period=30, n_values=3, maxi=5, mini=0)
