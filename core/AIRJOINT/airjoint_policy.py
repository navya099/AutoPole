from core.AIRJOINT.airjoint_cluster import AirJointCluster


class AIRJOINTPolicy:
    def decide(self, cluster: AirJointCluster, dataloader):
        result = {}

        for i, pole in enumerate(cluster.poles):
            if i in (0, 4):  # 1번, 5번
                result[pole] = [self._reinforced_bracket(pole, dataloader)]
            else:
                result[pole] = []

        return result