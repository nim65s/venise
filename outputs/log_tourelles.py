from .log import SortieLog, logger_parser


class LogTourelles(SortieLog):
    def log(self, logger, vc, vm, **kwargs):
        logger.info([vc, vm])

if __name__ == '__main__':
    logger_parser.set_defaults(logger='tourelles', period=0)
    LogTourelles(**vars(logger_parser.parse_args())).run()
