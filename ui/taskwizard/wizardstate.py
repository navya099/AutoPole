import tkinter as tk
# ----------------------------
# 상태 관리 클래스
# ----------------------------
class WizardState:
    def __init__(self):
        self.file_paths = [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
        ]
        # 다른 입력들도 같은 패턴
        self.inputs = [
           tk.IntVar(),
           tk.IntVar(),
           tk.DoubleVar(),
           tk.IntVar(),
        ]
        # ✅ Mode를 IntVar로
        self.mode = tk.IntVar(value=1)  # 0 = 기존 노선용

    # -----------------------------
    # Step별 유효성 검사
    # -----------------------------
    def validate_step(self, step: int) -> tuple[bool, str]:
        if step == 0:
            return self._validate_files()
        if step == 1:
            return self._validate_mode()
        if step == 2:
            return self._validate_inputs()
        return True, ""

    # -----------------------------
    # 내부 검증 함수
    # -----------------------------
    def _validate_files(self):
        for path in self.file_paths:
            if not path.get():
                return False, "모든 파일을 선택하세요."
        return True, ""

    def _validate_mode(self):
        if self.mode.get() not in (0, 1):
            return False, "모드를 선택하세요."
        return True, ""

    def _validate_inputs(self):
        speed = self.inputs[0].get()
        linecount = self.inputs[1].get()
        offset = self.inputs[2].get()
        direction = self.inputs[3].get()

        if speed not in (150, 250, 350):
            return False, "설계속도는 150 / 250 / 350 중 하나여야 합니다."

        if linecount <= 0:
            return False, "선로 갯수는 1 이상이어야 합니다."

        if offset <= 0:
            return False, "선로 중심간격은 0보다 커야 합니다."

        if direction not in (-1, 1):
            return False, "폴 방향은 -1 또는 1 이어야 합니다."

        return True, ""