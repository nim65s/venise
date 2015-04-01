from argparse import ArgumentParser

from .sonde import Sonde, sonde_parser


class Granier(Sonde):
    pass

granier_parser = ArgumentParser(parents=[sonde_parser], add_help=False)
granier_parser.set_defaults(nom='granier', period=10, n_values=3, maxi=5, mini=0)
