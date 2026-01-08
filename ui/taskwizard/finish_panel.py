from ui.taskwizard.steppanels import StepPanel
import tkinter as tk

class FinishPanel(StepPanel):
    def show(self):
        tk.Label(self.master, text="마침", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.master, text="모든 작업이 끝났습니다!", font=("Arial", 12)).pack(pady=10)
