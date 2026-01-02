from core.AIRJOINT.airjoint_policy import AIRJOINTPolicy
from core.BRACKET.bracket_policy import BracketPolicy
from core.base_manager import BaseManager
from core.section.section_type import SectionType
from utils.logger import logger

class BracketManager(BaseManager):
    def __init__(self, airjoint_clusters, dataloader, polecollection):
        super().__init__(dataloader)
        self.collection = polecollection
        self.airjoint_clusters = airjoint_clusters

        logger.debug("BracketManager 초기화 완료")

    def run(self):
        self._build_normal_brackets()
        self._build_airjoint_brackets()
        logger.debug("브래킷 생성 완료")

    def _build_normal_brackets(self):
        policy = BracketPolicy()
        """일반 정책용 브래킷"""
        for group_index, group in enumerate(self.collection):
            for pole in group:
                #섹션이 에어조인트이면 걸러짐
                if pole.current_section == SectionType.AIRJOINT:
                    continue
                try:  # pole 순회
                    specs = policy.decide(group_index, pole, self.loader.databudle.designspeed)
                    pole.brackets.extend(specs)
                except Exception:
                    logger.exception(f"Bracket 생성 실패 (index={group_index})")

    def _build_airjoint_brackets(self):

        """에어조인트 정책용 브래킷"""
        pole_map = {
            pole.pos: pole
            for group in self.collection
            for pole in group
        }
        group_index_map = {
            pole.pos: group_index
            for group_index, group in enumerate(self.collection)
            for pole in group
        }

        aj_policy = AIRJOINTPolicy()
        #이미 기본 정책에서 에어조인트구간만 판별함
        for cluster in self.airjoint_clusters:
            results = aj_policy.decide_airjoint(cluster, pole_map,group_index_map, self.loader.databudle.designspeed)

            for pos, specs in results.items():
                pole = pole_map.get(pos)
                if not pole:
                    logger.warning(f"AIRJOINT pole 누락: pos={pos}")
                    continue

                pole.brackets.extend(specs)