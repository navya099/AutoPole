from core.FEEDER.feeder_policy import FeederPolicy
from core.base_manager import BaseManager
from utils.logger import logger

class FeederManager(BaseManager):
    """급전선 설비(전선x) 데이터를 설정하는 클래스"""

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)
        logger.debug(f'FeederManager 초기화 완료')
    def run(self):
        self.create_feeder()
        logger.debug(f'급전선 생성 완료')
    def create_feeder(self):
        policy = FeederPolicy()
        speed = self.loader.databudle.designspeed

        for pole in self.poledata.poles:
            spec = policy.decide(pole, speed)
            pole.apply_feeder(spec)
