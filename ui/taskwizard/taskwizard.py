import tkinter as tk
import queue
from tkinter import messagebox

from ui.taskwizard.design_context import DesignContext
from ui.taskwizard.fileselect import FileSelectionPanel
from ui.taskwizard.finish_panel import FinishPanel
from ui.taskwizard.inputpanle import InputPanel
from ui.taskwizard.modeselct import ModeSelectionPanel
from ui.taskwizard.proecseeing import ProcessingPanel
from ui.taskwizard.wizardstate import WizardState

# ----------------------------
# 메인 Wizard
# ----------------------------
class TaskWizard(tk.Toplevel):
    def __init__(self, master, subject, debug=False):
        super().__init__(master)
        self.debug = debug
        self.state = WizardState()
        self.design_context = DesignContext()
        self.subject = subject  # Observer 패턴 연결
        self.queue = queue.Queue()
        self.worker = None
        self.step = 0
        self.title("전주 생성 마법사")
        self.geometry("500x500")

        # ✅ content 영역
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # ✅ button 영역
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", pady=10)

        self.prev_btn = tk.Button(self.button_frame, text="이전", command=self.prev_step)
        self.next_btn = tk.Button(self.button_frame, text="다음", command=self.next_step)
        self.cancel_btn = tk.Button(self.button_frame, text="취소", command=self.cancel)

        self.prev_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.cancel_btn.pack(side="right", padx=5)

        # ✅ 패널 목록
        self.panels = [
            FileSelectionPanel(self.content_frame, self.state),
            ModeSelectionPanel(self.content_frame, self.state),
            InputPanel(self.content_frame, self.state),
            ProcessingPanel(
                self.content_frame,
                self.state,
                self.design_context,
                on_finished=self.on_processing_finished
            ),
            FinishPanel(self.content_frame, self.state)
        ]

        self.update_step()

    # -----------------------------
    # Step Control
    # -----------------------------
    def update_step(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        self.panels[self.step].show()

        # 버튼 상태 제어
        self.prev_btn.config(state="normal" if self.step > 0 else "disabled")

        if self.step < len(self.panels) - 1:
            self.next_btn.config(text="다음", command=self.next_step)
        else:
            self.next_btn.config(text="완료", command=self.finish_wizard)

    def next_step(self):
        valid, message = self.state.validate_step(self.step)

        if not valid:
            messagebox.showwarning("입력 오류", message)
            return

        # 🔴 입력 확정 타이밍
        if self.step == 2:  # InputPanel → ProcessingPanel
            self.commit_inputs_to_context()

        self.step += 1
        self.update_step()

    def prev_step(self):
        if self.step > 0:
            self.step -= 1
            self.update_step()

    # -----------------------------
    # Processing 완료 콜백
    # -----------------------------
    def on_processing_finished(self):
        self.step = 4
        self.update_step()

    # -----------------------------
    # 종료
    # -----------------------------
    def cancel(self):
        self.destroy()

    def finish_wizard(self):
        self.subject.result = self.design_context  # Subject를 통해 MainWindow 갱신
        self.destroy()

    def commit_inputs_to_context(self):
        self.design_context.speed = self.state.inputs[0].get()
        self.design_context.offset = self.state.inputs[2].get()
        self.design_context.direction = self.state.inputs[3].get()

