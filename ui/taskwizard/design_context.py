# ----------------------------
# 설계결과 보관 클래스
# ----------------------------
class DesignContext:
    def __init__(self):
        self.speed = None
        self.refdata = None
        self.poledata = None
        self.wiredata = None
        self.irs = []
        is_processed: bool = False
