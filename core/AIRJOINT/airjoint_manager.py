from core.AIRJOINT.airjoint_cluster import AirJointCluster
from core.AIRJOINT.airjoint_enum import AirJoint

class AirjointManager:
    @staticmethod
    def define_airjoint_clusters(
        positions: list[int],
        airjoint_span: int = 1600,
        tolerance: int = 100
    ) -> list[AirJointCluster]:

        clusters: list[AirJointCluster] = []

        def is_near_multiple(pos: int) -> bool:
            r = pos % airjoint_span
            return pos > airjoint_span and (
                r <= tolerance or r >= airjoint_span - tolerance
            )

        i = 0
        cluster_idx = 1

        while i <= len(positions) - 6:
            if is_near_multiple(positions[i]):
                cluster_positions = positions[i + 1:i + 6]

                clusters.append(
                    AirJointCluster(
                        number=f'AJ-{cluster_idx}',
                        positions=cluster_positions
                    )
                )
                cluster_idx += 1
                i += 5
            else:
                i += 1

        return clusters
