if __name__ == '__main__':
    from .points import trajectoire_points_parser as parser
    from ..settings import PROD

    if PROD:
        from .granier import TrajectoireGranier as Trajectoire
    else:
        from .partout import TrajectoirePartout as Trajectoire, trajectoire_destination_parser as parser

    Trajectoire(**vars(parser.parse_args())).run()
