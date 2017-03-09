if __name__ == '__main__':
    from .destination import trajectory_destination_parser as parser
    from .mona import MonaTrajectory as Trajectory

    Trajectory(**vars(parser.parse_args())).run()
