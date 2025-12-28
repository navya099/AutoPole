from ui.taskwizard.steppanels import StepPanel
import tkinter as tk

class ModeSelectionPanel(StepPanel):
    def show(self):
        self.clear()
        tk.Label(self.master, text="단계2: 모드 선택", font=("Arial", 14)).pack(pady=10)
        self.state.mode = tk.StringVar(value=self.state.mode)
        for mode in ['기존 노선용', '새 노선용']:
            tk.Radiobutton(self.master, text=mode, variable=self.state.mode, value=mode).pack(pady=5)