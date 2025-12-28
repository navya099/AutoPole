# ----------------------------
# 상태 관리 클래스
# ----------------------------
class WizardState:
    def __init__(self):
        self.file_paths = [None]*4
        self.inputs = [None]*4
        self.mode = None