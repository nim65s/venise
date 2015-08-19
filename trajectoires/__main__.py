if __name__ == '__main__':
    from ..settings import PROD

    if PROD:
        from .points import trajectoire_points_parser as parser
        from .granier import TrajectoireGranier as Trajectoire
    else:
        from .destination import trajectoire_destination_parser as parser
        from .partout import TrajectoirePartout as Trajectoire

    Trajectoire(**vars(parser.parse_args())).run()
