from core.MAST.mast_builder import MastBuilder
from core.MAST.mast_policy import MastPolicy
from core.POLE.poledata import PolePlaceDATA
from core.POLE.polegroup_manager import PoleGroupManager
from core.POLE.polegroup import PoleGroup
from core.base_manager import BaseManager
from utils.util import Direction
from utils.logger import logger

class MastManager(BaseManager):
    def __init__(self, dataloader, polerefdatas):
        super().__init__(dataloader)
        self.poledatas: PoleGroupManager = PoleGroupManager()
        self.polerefdatas = polerefdatas


    def run(self):

        policy = MastPolicy()
        speed = self.loader.databudle.designspeed
        track_count = self.loader.databudle.linecount


        base_direction = (
            Direction.LEFT if self.loader.databudle.poledirection == -1
            else Direction.RIGHT
        )

        builder = MastBuilder()
        for ref in self.polerefdatas:
            group = self.poledatas.new_group(ref.pos)
            for track_idx in range(track_count):
                try:
                    pole = builder.build(
                        ref=ref,
                        track_idx=track_idx,
                        base_direction=base_direction,
                        policy=policy,
                        speed=speed
                    )
                    group.add_pole(track_idx, pole)
                except Exception:
                    logger.exception(
                        f"Mast 생성 실패 (pos={ref.pos}, track={track_idx})"
                    )