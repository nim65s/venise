from datetime import datetime, timedelta

from .processor import Processor, processor_parser

DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class IsUp(Processor):
    def process(self, last_seen_agv, **kwargs):
        try:
            dt = datetime.strptime(last_seen_agv, DT_FORMAT)
            is_up = (datetime.now() - dt) < timedelta(seconds=2)
        except:
            is_up = False
        return {'is_up': is_up}


if __name__ == '__main__':
    IsUp(**vars(processor_parser.parse_args())).run()
