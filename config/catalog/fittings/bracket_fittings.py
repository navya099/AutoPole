from config.catalog.fittings.fitting_materail import FittingMaterial
from config.catalog.fittings.fitting_role import FittingRole
class FittingCatalog:
    _dic = {
        150: {
            FittingRole.AIRJOINT_MESSENGER: FittingMaterial(499, "에어조인트용 조가선 지지금구"),
            FittingRole.INVALID_LIFT_MESSENGER: FittingMaterial(1292, "무효인상용 조가선 지지금구"),
            FittingRole.INVALID_LIFT_CONTACT: FittingMaterial(1295, "무효인상용 전차선 지지금구"),
            FittingRole.STEADYARM_LEFT: FittingMaterial(1293, "곡선당김금구L"),
            FittingRole.STEADYARM_RIGHT: FittingMaterial(1294, "곡선당김금구R"),
        },
        250: {
            FittingRole.AIRJOINT_MESSENGER: FittingMaterial(1279, "에어조인트용 조가선 지지금구"),
            FittingRole.INVALID_LIFT_MESSENGER: FittingMaterial(1281, "무효인상용 조가선 지지금구"),
            FittingRole.INVALID_LIFT_CONTACT: FittingMaterial(1282, "무효인상용 전차선 지지금구"),
            FittingRole.STEADYARM_LEFT: FittingMaterial(1280, "곡선당김금구L"),
            FittingRole.STEADYARM_RIGHT: FittingMaterial(1283, "곡선당김금구R"),
        },
        350: {
            FittingRole.AIRJOINT_MESSENGER: FittingMaterial(586, "에어조인트용 조가선 지지금구"),
            FittingRole.INVALID_LIFT_MESSENGER: FittingMaterial(584, "무효인상용 조가선 지지금구"),
            FittingRole.INVALID_LIFT_CONTACT: FittingMaterial(585, "무효인상용 전차선 지지금구"),
            FittingRole.STEADYARM_LEFT: FittingMaterial(576, "곡선당김금구L"),
            FittingRole.STEADYARM_RIGHT: FittingMaterial(577, "곡선당김금구R"),
        }
    }

    REQUIRED_ROLES = {
        FittingRole.AIRJOINT_MESSENGER,
        FittingRole.INVALID_LIFT_MESSENGER,
        FittingRole.INVALID_LIFT_CONTACT,
        FittingRole.STEADYARM_LEFT,
        FittingRole.STEADYARM_RIGHT,
    }
    @classmethod
    def get(cls, speed: int, role: FittingRole) -> FittingMaterial:
        try:
            return cls._dic[speed][role]
        except KeyError as e:
            raise ValueError(
                f"FittingMaterial not defined: speed={speed}, role={role}"
            ) from e

    @classmethod
    def validate(cls):
        for speed, items in cls._dic.items():
            missing = cls.REQUIRED_ROLES - items.keys()
            if missing:
                raise RuntimeError(
                    f"Speed {speed} missing fitting roles: {missing}"
                )
