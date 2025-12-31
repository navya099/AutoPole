
from core.BRACKET.bracket_policy import BracketPolicy
from core.POLE.polegroup_collector import PoleGroupCollection
from core.base_manager import BaseManager
from utils.logger import logger

class BracketManager(BaseManager):
    """
     가동브래킷매니저 BaseManager상속
    """

    def __init__(self, dataloader, polecollection: PoleGroupCollection):
        super().__init__(dataloader)
        self.collecton = polecollection
        logger.debug(f'BracketManager 초기화 완료')

    def run(self):
        self.create_bracket()
        logger.debug(f'Bracket생성 완료')

    def create_bracket(self):
        policy = BracketPolicy()
        for group_index, group in enumerate(self.collecton):
            for pole in group:
                try:# pole 순회
                    spec = policy.decide(
                        index=group_index,  # 그룹 단위 index 사용
                        pole=pole,
                        dataloader=self.loader
                    )
                    pole.apply_bracket(spec)
                except Exception:
                    logger.exception(f"Bracket 생성 실패 (index={group_index})")