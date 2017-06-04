if __name__ == '__main__':
    # from .destination import trajectory_destination_parser as parser
    # from .mona import MonaTrajectory as Trajectory
    from .random_destination import RandomDestination as Trajectory, random_destination_parser as parser

    Trajectory(**vars(parser.parse_args())).run()
