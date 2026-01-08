from ui.taskwizard.steppanels import StepPanel
import tkinter as tk


class ModeSelectionPanel(StepPanel):
    def show(self):
        self.clear()

        tk.Label(
            self.master,
            text="단계2: 모드 선택",
            font=("Arial", 14)
        ).pack(pady=10)

        var = self.state.mode

        tk.Radiobutton(
            self.master,
            text="기존 노선용",
            variable=var,
            value=0
        ).pack(pady=5)

        tk.Radiobutton(
            self.master,
            text="새 노선용",
            variable=var,
            value=1
        ).pack(pady=5)
