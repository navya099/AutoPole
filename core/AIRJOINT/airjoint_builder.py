from core.AIRJOINT.airjoint_cluster import AirJointCluster
from core.section.section_type import SectionType
from core.POLE.polegroup_collector import PoleGroupCollection

class AirjointBuilder:
    @staticmethod
    def build_airjoint_clusters(
        polecollection: PoleGroupCollection
    ) -> list[AirJointCluster]:

        clusters: list[AirJointCluster] = []
        buffer = []

        poles = sorted(
            polecollection.iter_poles(),
            key=lambda p: p.pos
        )

        for pole in poles:
            if pole.current_section == SectionType.AIRJOINT:
                buffer.append(pole)

                if len(buffer) == 5:
                    clusters.append(AirJointCluster(buffer))
                    buffer = []
            else:
                buffer = []

        # AIRJOINT는 반드시 5개 단위 → 나머지는 무시
        return clusters
