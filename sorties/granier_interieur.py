from numpy import array
from ..vmq import vmq_parser, Subscriber, Pusher
from ..settings import Hote


class SortieGranierInterieur(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hote = Hote.moro
        self.hotes = [Hote.ame, Hote.yuki]

    def loop(self):
        self.data[self.hote]['granier'] = array([self.data[h]['granier'] for h in self.hotes]).mean(axis=0).tolist()
        self.push.send_json([self.hote, {'granier': self.data[self.hote]['granier']}])


if __name__ == '__main__':
    SortieGranierInterieur(**vars(vmq_parser.parse_args())).run()
