from core.AIRJOINT.airjoint_manager import AirjointManager
from core.POLE.pole_refdata import PoleRefData
from core.POLE.pole_utils import PoleUtils
from geometryor.interpolator import CoordinateInterpolator

from point3d import Point3d


class PolePositionBuilder:
    def __init__(self, loader):
        self.loader = loader
        self.intpoler = CoordinateInterpolator(self.loader.bvealignment)
    def build(self, pos: int, span: int):
        pole = PoleRefData()
        pole.pos = pos
        pole.span = span
        pole.structure_type = self.loader.structures.get_structure_type_at(pos)
        pole.curve_type = self.loader.bvealignment.get_current_curve_string(pos)
        pole.radius = float(self.loader.bvealignment.get_curve_radius(pos))
        pole.cant = float(self.loader.bvealignment.get_curve_cant(pos))
        pole.pitch = float(self.loader.bvealignment.get_pitch_permille(pos))

        self.intpoler.cal_interpolate(pos)
        center_coord = self.intpoler.get_pos_coord()
        pole.center_coord = Point3d(center_coord.x, center_coord.y, center_coord.z)
        pole.azimuth = self.intpoler.get_vector()

        return pole
