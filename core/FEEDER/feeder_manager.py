from core.base_manager import BaseManager


class FeederManager(BaseManager):
    """급전선 설비(전선x) 데이터를 설정하는 클래스"""

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)

    def run(self):
        self.create_feeder()

    def create_feeder(self):
        data = self.poledata
        speed = self.loader.databudle.designspeed
        # 구조별 설계속도에 따른 피더 인덱스 맵
        feeder_map = {
            ('토공', 150): 1234,
            ('토공', 250): 1234,
            ('토공', 350): 597,
            ('교량', 150): 1234,
            ('교량', 250): 1234,
            ('교량', 350): 597,
            ('터널', 150): 1249,
            ('터널', 250): 1249,
            ('터널', 350): 598,
        }

        for i in range(len(data.poles)):
            current_structure = data.poles[i].current_structure

            feederindex = feeder_map.get((current_structure, speed), 1234)
            data.poles[i].feeder.index = feederindex
            data.poles[i].feeder.name = '급전선 지지물'
            data.poles[i].feeder.direction = data.poles[i].direction
            data.poles[i].feeder.positionx = data.poles[i].gauge * data.poles[i].feeder.direction.value