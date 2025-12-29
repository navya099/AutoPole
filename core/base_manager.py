from typing import Optional

from fileio.dataloader import DataLoader


class BaseManager:
    """MastManager와 BracketManager의 공통 기능을 관리하는 부모 클래스
    Attributes:
        loader (DataLoader): 데이터로더 객체
    """
    def __init__(self, dataloader: DataLoader):
        self.loader = dataloader  # ✅ DataLoader 인스턴스를 가져옴