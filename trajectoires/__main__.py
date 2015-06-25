if __name__ == '__main__':
    from .points import trajectoire_points_parser as parser
    from ..settings import PROD

    if PROD:
        from .demo import TrajectoireDemo as Trajectoire
    else:
        from .granier import TrajectoireGranier as Trajectoire

    Trajectoire(**vars(parser.parse_args())).run()
