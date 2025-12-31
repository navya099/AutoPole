from core.POLE.pole_file_source import PoleFileSource
from core.POLE.polegroup_collector import PoleGroupCollection
from core.POLE.poleplace_builder import PolePlaceBuilder
from core.base_manager import BaseManager
from utils.util import Direction
from utils.logger import logger

class PolePlaceDATAManager(BaseManager):
    def __init__(self, dataloader, polerefdatas):
        super().__init__(dataloader)
        self.poledatas: PoleGroupCollection = PoleGroupCollection()
        self.polerefdatas = polerefdatas


    def run(self):
        self.excute_polerefdata_builder()
        self.apply_post_number_strategy()

    def excute_polerefdata_builder(self):
        track_count = self.loader.databudle.linecount

        base_direction = (
            Direction.LEFT if self.loader.databudle.poledirection == -1
            else Direction.RIGHT
        )

        builder = PolePlaceBuilder()
        for ref in self.polerefdatas:
            group = self.poledatas.new_group(ref.pos)
            for track_idx in range(track_count):
                try:
                    pole = builder.build(
                        ref=ref,
                        track_idx=track_idx,
                        base_direction=base_direction
                    )
                    group.add_pole(track_idx, pole)
                except Exception:
                    logger.exception(
                        f"Pole 생성 실패 (pos={ref.pos}, track={track_idx})"
                    )

    def apply_post_number_strategy(self):
        if self.loader.databudle.mode == 1:
            # 자동 생성
            self._apply_auto_post_numbers()
        else:
            # 외부 데이터 사용
            self._apply_external_post_numbers(PoleFileSource())

    def _apply_auto_post_numbers(self):
        self.poledatas.update_post_numbers()

    def _apply_external_post_numbers(self, source):

        data = source.load()
        self.post_number_lst = data.post_numbers


