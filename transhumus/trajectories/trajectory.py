from math import atan2, copysign, cos, hypot, pi, sin

from numpy import array

from ..settings import BOUNDARIES, SMOOTH_SPEED, SPEED_MEAN_MAX, WHEEL_POS
from ..utils.dist_angles import dist_angle
from ..utils.point_in_polygon import wn_pn_poly
from .base_trajectory import BaseTrajectory


class Trajectory(BaseTrajectory):
    def smooth_speed(self, smoothe_speed, v, w, t, vg, wg, tg, **kwargs):
        if smoothe_speed:
            dv, dw, dt = v - vg, w - wg, dist_angle(t, tg)
            return {
                'v': round(v - copysign(SMOOTH_SPEED['v'], dv), 5) if abs(dv) > SMOOTH_SPEED['v'] else vg,
                'w': round(w - copysign(SMOOTH_SPEED['w'], dw), 5) if abs(dw) > SMOOTH_SPEED['w'] else wg,
                't': round((t - copysign(SMOOTH_SPEED['t'], dt)) % (2 * pi), 5) if abs(dt) > SMOOTH_SPEED['t'] else tg,
            }
        return {'v': vg, 'w': wg, 't': tg}

    def turret(self, wheel_pos, v, w, t, **kwargs):
        vit_x = v * cos(t) - w * sin(wheel_pos)
        vit_y = v * sin(t) + w * cos(wheel_pos)
        return round(atan2(vit_y, vit_x) % (2 * pi), 5), round(SPEED_MEAN_MAX * hypot(vit_x, vit_y), 5)

    def process_turrets(self, **kwargs):
        tt, vt = zip(*[self.turret(WHEEL_POS[i], **kwargs) for i in range(3)])
        vt = array(vt)
        return {'tt': tt, 'vt': [round(v, 5) for v in (vt * 2 * SPEED_MEAN_MAX / abs(vt).max()).tolist()]
                if abs(vt).max() != 0 else [0, 0, 0]}

    def inside(self, host, x, y, **kwargs):
        return {'inside': wn_pn_poly((x, y), BOUNDARIES[host]) != 0}
