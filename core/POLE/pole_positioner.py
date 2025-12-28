from core.AIRJOINT.airjoint_manager import AirjointManager
from core.POLE.pole_file_source import PoleFileSource
from core.POLE.pole_processor import PoleBuilder
from core.POLE.pole_utils import PoleUtils
from core.POLE.poledata import PoleDATA
from core.POLE.poledata_manager import PoleDATAManager
from core.base_manager import BaseManager
from utils.logger import logger
from utils.util import Direction

class PolePositionManager(BaseManager):
    """전주 생성기능을 관리하는 클래스

    Attributes:
        pole_positions (list): 전주 위치 데이터
        airjoint_list (list): 에어조인트 위치 데이터
        post_number_lst (list): 전주번호 데이터
        posttype_list (list): 전주타입 리스트
    """

    def __init__(self, dataloader):
        super().__init__(dataloader)
        self.pole_positions: list[int] = []
        self.airjoint_list: list[tuple[int, str]] = []
        self.post_number_lst: list[str] = []
        self.posttype_list: list[tuple[int, str]] = []
        logger.debug(f'PolePositionManager 초기화 완료')

    def run(self):
        self.generate_positions()
        self.create_pole()

    def generate_positions(self):
        if self.loader.databudle.mode == 1:
            self._generate_auto()
        else:
            self._load_from_source(PoleFileSource())

        logger.info(
            f"[Pole] positions={len(self.pole_positions)}, "
            f"airjoints={len(self.airjoint_list)}, "
            f"post_numbers={len(self.post_number_lst)}"
        )

    def create_pole(self):
        data = PoleDATAManager()
        builder = PoleBuilder(self.loader)

        direction = (
            Direction.LEFT if self.loader.databudle.poledirection == -1
            else Direction.RIGHT
        )

        for i, pos in enumerate(self.pole_positions):
            try:
                span = (
                    self.pole_positions[i + 1] - pos
                    if i < len(self.pole_positions) - 1 else 0
                )

                pole = data.new_pole()

                builder.build(
                    pole,
                    pos,
                    span,
                    self.airjoint_list,
                    self.post_number_lst,
                    direction
                )

            except Exception:
                logger.exception(f"create_pole 실패 (index={i}, pos={pos})")

        self.poledata = data if data.poles else None

    def _generate_auto(self):

        """자동 포지션 생성 메소드 """
        self.pole_positions = PoleUtils.distribute_pole_spacing_flexible( self.loader.bvealignment.startkm, self.loader.bvealignment.endkm, spans=(45, 50, 55, 60) )
        self.airjoint_list = AirjointManager.define_airjoint_section(self.pole_positions)
        self.post_number_lst = PoleUtils.generate_postnumbers(self.pole_positions)


    def _load_from_source(self, source):
        """외부로부터 포지션 생성 메서드"""
        data = source.load()
        self.pole_positions = data.positions
        self.post_number_lst = data.post_numbers
        self.posttype_list = data.post_types
        self.airjoint_list = data.airjoints

