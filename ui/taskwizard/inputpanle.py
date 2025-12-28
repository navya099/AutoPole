from ui.taskwizard.steppanels import StepPanel
import tkinter as tk
from tkinter import ttk
class InputPanel(StepPanel):
    def show(self):
        self.clear()
        tk.Label(self.master, text="단계3: 입력값", font=("Arial", 14)).pack(pady=10)
        labels = ['설계속도','선로 갯수','선로중심간격','폴 방향']
        combo_options = {0:['150','250','350'],3:['-1','1']}
        self.vars = []
        for i, label in enumerate(labels):
            frame = tk.Frame(self.master)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{label}:").pack(side="left")
            var = tk.StringVar(value=self.state.inputs[i])
            self.state.inputs[i] = var
            if i in combo_options:
                cb = ttk.Combobox(frame, values=combo_options[i], textvariable=var, state="readonly")
                cb.pack(side="left", padx=5)
                cb.current(0)
            else:
                tk.Entry(frame, textvariable=var).pack(side="left", padx=5)