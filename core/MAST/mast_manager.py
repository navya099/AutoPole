from core.MAST.mast_builder import MastBuilder
from core.MAST.mast_policy import MastPolicy
from core.base_manager import BaseManager
from utils.util import Direction
from utils.logger import logger

class MastManager(BaseManager):
    def __init__(self, dataloader, polecollection):
        super().__init__(dataloader)
        self.collection = polecollection

    def run(self):
        policy = MastPolicy()
        speed = self.loader.databudle.designspeed
        builder = MastBuilder(policy)

        for pole in self.collection.iter_poles():
            try:
                builder.apply(pole, speed)
            except Exception:
                logger.exception(
                    f"Mast 생성 실패 (pos={pole.pos}, track={pole.track_index})"
                )
