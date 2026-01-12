from line3d import Line3d
from utils.Vector3 import Vector3

class WireGeometry(Line3d):
    def __init__(self, start,end):
        super().__init__(start,end)
        """전선 지오메트리
        Attributes:
            vertor3d: 전선의 3D방향벡터
            sag: 전선의 새그
        """
        self.vector3d = Vector3(
            end.x - start.x,
            end.y - start.y,
            end.z - start.z
        )
        self.sag: float = 0.0
    @property
    def plan_angle(self):
        return self.vector3d.plan_angle()

    @property
    def slope_angle(self):
        return self.vector3d.slope_angle()

