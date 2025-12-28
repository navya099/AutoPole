from core.AIRJOINT.airjoint_manager import AirjointManager
from core.POLE.pole_utils import PoleUtils
from core.POLE.poledata import PoleDATA


class PoleBuilder:
    def __init__(self, loader):
        self.loader = loader

    def build(self, pole: PoleDATA, pos: int, span: int,
              airjoint_list, post_number_lst, direction):
        pole.pos = pos
        pole.span = span
        pole.current_structure = self.loader.structures.get_structure_type_at(pos)
        pole.current_curve = self.loader.bvealignment.get_current_curve_string(pos)
        pole.radius = float(self.loader.bvealignment.get_curve_radius(pos))
        pole.cant = float(self.loader.bvealignment.get_curve_cant(pos))
        pole.pitch = float(self.loader.bvealignment.get_pitch_permille(pos))
        pole.current_airjoint = AirjointManager.check_isairjoint(pos, airjoint_list)
        pole.post_number = PoleUtils.find_post_number(post_number_lst, pos)
        pole.direction = direction
