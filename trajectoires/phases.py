from argparse import ArgumentParser
from datetime import datetime

from .points import trajectoire_points_parser
from .granier import TrajectoireGranier

from ..settings import Hote, Phase, BERCAIL, MORNING


class TrajectoirePhases(TrajectoireGranier):
    def __init__(self, phase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phase = Phase[phase]
        if phase == Phase.auto:
            phase = Phase.tourne if 10 <= datetime.now().hour <= 17 else Phase.parking
        self.phase = phase

    def tourne(self, hote):
        return hote == Hote.moro and self.phase != Phase.parking or \
                hote == Hote.ame and Phase.sort_ame < self.phase < Phase.rentre_ame or \
                hote == Hote.yuki and Phase.sort_yuki < self.phase < Phase.rentre_yuki

    def get_w(self, hote, **kwargs):
        if self.tourne(hote):
            return super().get_w(**self.data[hote])
        return 0

    def process_speed(self, hote, destination, x, y, state, **kwargs):
        if self.tourne(hote):
            if state == 32 and hote == Hote.ame and self.phase == Phase.tourne and datetime.now().hour == 17:
                print('Fin de la journée… Rentre ame')
                self.phase = Phase.rentre_ame
                return self.rentre_ame()
            else:
                return super().process_speed(**self.data[hote])
        elif self.phase == Phase.parking:
            if datetime.now().hour == 9 and hote == Hote.yuki:
                print('Début de la journée… Sort yuki')
                self.phase = Phase.sort_yuki
                return self.sort_yuki()
            return {'v': 0, 'w': 0, 'stop': True}
        elif self.phase == Phase.sort_yuki:
            if hote == Hote.yuki and self.distance(destination, x, y) < 1:
                print('Yuki est sorti… Sort ame')
                self.phase = Phase.sort_ame
                self.sort_ame()
                return {'boost': False}
            elif hote == Hote.ame:
                return {'v': 0, 'w': 0, 'stop': True}
        elif self.phase == Phase.sort_ame:
            if hote == Hote.ame and self.distance(destination, x, y) < 1:
                print('Ame est sorti… Go !')
                self.phase = Phase.tourne
                return {'boost': False}
        elif self.phase == Phase.rentre_ame:
            if hote == Hote.ame and self.distance(destination, x, y) < 0.5:
                print('Ame est renté… Rentre yuki')
                self.phase = Phase.rentre_yuki
                return {'boost': False, 'v': 0, 'w': 0, 'stop': True}
        elif self.phase == Phase.rentre_yuki:
            if hote == Hote.yuki and self.distance(destination, x, y) < 0.5:
                print('Yuki est rentré… Bonne nuit !')
                self.phase = Phase.parking
                return {'boost': False, 'v': 0, 'w': 0, 'stop': True}
            elif hote == Hote.ame:
                return {'boost': False, 'v': 0, 'w': 0, 'stop': True}
        return self.go_to_point(**self.data[hote])

    def sort_yuki(self):
        self.data[Hote.yuki].update(destination=MORNING[Hote.yuki], boost=True, state=12)
        return self.go_to_point(**self.data[hote])

    def rentre_yuki(self):
        self.data[Hote.yuki].update(destination=BERCAIL[Hote.yuki])
        return self.go_to_point(**self.data[hote])

    def sort_ame(self):
        self.data[Hote.ame].update(destination=MORNING[Hote.ame], boost=True, state=32)
        return self.go_to_point(**self.data[hote])

    def rentre_ame(self):
        self.data[Hote.ame].update(destination=BERCAIL[Hote.ame])
        return self.go_to_point(**self.data[hote])


trajectoire_phases_parser = ArgumentParser(parents=[trajectoire_points_parser], conflict_handler='resolve')
trajectoire_phases_parser.add_argument('-P', '--phase', help="phase", default=Phase.auto, choices=[p.name for p in Phase])

if __name__ == '__main__':
    TrajectoirePhases(**vars(trajectoire_phases_parser.parse_args())).run()
