import tkinter as tk
import queue

from ui.taskwizard.fileselect import FileSelectionPanel
from ui.taskwizard.inputpanle import InputPanel
from ui.taskwizard.modeselct import ModeSelectionPanel
from ui.taskwizard.proecseeing import ProcessingPanel
from ui.taskwizard.taskworker import TaskWorker
from ui.taskwizard.wizardstate import WizardState


# ----------------------------
# 메인 Wizard
# ----------------------------
class TaskWizard(tk.Toplevel):
    def __init__(self, master, debug=False):
        super().__init__(master)
        self.debug = debug
        self.state = WizardState()
        self.queue = queue.Queue()
        self.worker = None
        self.step = 0
        self.title("전주 생성 마법사")
        self.geometry("500x500")

        self.panels = [
            FileSelectionPanel(self, self.state),
            ModeSelectionPanel(self, self.state),
            InputPanel(self, self.state),
            ProcessingPanel(self, self.state)
        ]

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", pady=10)
        tk.Button(self.button_frame, text="이전", command=self.prev_step).pack(side="left", padx=5)
        self.next_button = tk.Button(self.button_frame, text="다음", command=self.next_step)
        self.next_button.pack(side="left", padx=5)
        tk.Button(self.button_frame, text="취소", command=self.destroy).pack(side="right", padx=5)

        self.update_step()

    def update_step(self):
        """현재 단계 UI 업데이트"""
        # 기존 위젯 제거
        for widget in self.winfo_children():
            widget.destroy()

        # 각 단계별 UI 구성
        if self.step == 0:
            self.panels[0].show()
            self.enable_next_button(True)

        elif self.step == 1:
            self.panels[1].show()
        elif self.step == 2:
            self.panels[2].show()
            self.enable_next_button(True)  # 유효성 검사 후 '다음' 버튼 활성화
        elif self.step == 3:
            self.panels[3].show()
        elif self.step == 4:
            tk.Label(self, text="마침", font=("Arial", 14)).pack(pady=10)
            tk.Label(self, text="모든 작업이 끝났습니다!", font=("Arial", 12)).pack(pady=10)

        # 버튼 프레임
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        if self.step > 0:
            tk.Button(button_frame, text="이전", command=self.prev_step).pack(side="left", padx=5)

        # '다음' 버튼 초기화
        if self.next_button:
            self.next_button.destroy()  # 이전에 있던 next_button을 제거합니다.

        if self.step < 4:
            self.next_button = tk.Button(button_frame, text="다음", command=self.next_step)
            self.next_button.pack(side="left", padx=5)
        else:
            tk.Button(button_frame, text="완료", command=self.finish_wizard).pack(side="left", padx=5)

        tk.Button(button_frame, text="취소", command=self.cancel).pack(side="right", padx=5)

    def next_step(self):
        self.step += 1
        self.update_step()

    def prev_step(self):
        if self.step > 0:
            self.step -= 1
            self.update_step()

    def cancel(self):
        """마법사 종료"""
        self.destroy()

    def enable_next_button(self, state):
        """'다음' 버튼 활성화/비활성화"""
        if self.next_button and self.next_button.winfo_exists():  # Ensure button exists
            self.next_button.config(state="normal" if state else "disabled")

    def finish_wizard(self):
        """마법사 완료 후 창 닫기"""
        self.destroy()
