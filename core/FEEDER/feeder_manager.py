from core.FEEDER import feeder_policy
from core.FEEDER.feeder_policy import FeederPolicy
from core.FEEDER.tf_policy import TFPolicy
from core.base_manager import BaseManager
from utils.logger import logger

class FeederManager(BaseManager):
    """급전선 설비(전선x) 데이터를 설정하는 클래스"""

    def __init__(self, dataloader, polecollection):
        super().__init__(dataloader)
        self.collection = polecollection
        logger.debug(f'FeederManager 초기화 완료')

    def run(self):
        self.create_feeder()
        logger.debug(f'급전선 설비 생성 완료')

    def create_feeder(self):
        af_policy = FeederPolicy()
        tf_policy = TFPolicy()
        speed = self.loader.databudle.designspeed

        for pole in self.collection.iter_poles():
            specs = []
            specs += af_policy.decide(pole, speed)
            #specs += tf_policy.decide(pole, speed)

            pole.apply_feeder(specs)
