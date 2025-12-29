from core.MAST.mast_policy import MastPolicy
from core.base_manager import BaseManager
from utils.logger import logger

class MastManager(BaseManager):

    def run(self):
        policy = MastPolicy()
        speed = self.loader.databudle.designspeed

        for i, pole in enumerate(self.poledata.poles):
            try:
                spec = policy.decide(pole, speed)
                pole.apply_mast(spec)
            except Exception:
                logger.exception(f"Mast 생성 실패 (index={i}, 측점={pole.pos})")
