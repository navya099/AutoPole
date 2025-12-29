
from core.BRACKET.bracket_dictionary import Dictionaryofbracket
from core.BRACKET.bracket_policy import BracketPolicy
from core.base_manager import BaseManager
from utils.logger import logger

class BracketManager(BaseManager):
    """
     가동브래킷매니저 BaseManager상속
    """

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)
        logger.debug(f'BracketManager 초기화 완료')

    def run(self):
        self.create_bracket()
        logger.debug(f'Bracket생성 완료')

    def create_bracket(self):
        policy = BracketPolicy()
        for i, pole in enumerate(self.poledata.poles):
            try:
                spec = policy.decide(
                    index=i,
                    pole=pole,
                    dataloader=self.loader
                )
                pole.apply_bracket(spec)
            except Exception:
                logger.exception(f"Bracket 생성 실패 (index={i})")