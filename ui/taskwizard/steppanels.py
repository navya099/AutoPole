# ----------------------------
# 단계별 UI 패널
# ----------------------------
from ui.taskwizard.wizardstate import WizardState


class StepPanel:
    def __init__(self, master, state: WizardState):
        self.master = master
        self.state = state

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()