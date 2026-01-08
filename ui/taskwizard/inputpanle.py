from ui.taskwizard.steppanels import StepPanel
import tkinter as tk
from tkinter import ttk


class InputPanel(StepPanel):
    def show(self):
        self.clear()

        tk.Label(
            self.master,
            text="단계3: 입력값",
            font=("Arial", 14)
        ).pack(pady=10)

        labels = ['설계속도', '선로 갯수', '선로중심간격', '폴 방향']
        combo_options = {
            0: ['150', '250', '350'],  # designspeed
            3: ['-1', '1']            # poledirection
        }

        for i, label in enumerate(labels):
            frame = tk.Frame(self.master)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{label}:").pack(side="left")

            # ✅ WizardState에 이미 있는 Var 재사용
            var = self.state.inputs[i]

            if i in combo_options:
                cb = ttk.Combobox(
                    frame,
                    values=combo_options[i],
                    textvariable=var,
                    state="readonly",
                    width=10
                )
                cb.pack(side="left", padx=5)

                # ✅ 값이 없을 때만 기본값 설정
                if not var.get():
                    cb.current(0)
            else:
                vcmd = self.master.register(self._validate_number)
                tk.Entry(
                    frame,
                    textvariable=var,
                    validate="key",
                    validatecommand=(vcmd, "%P"),
                    width=12
                ).pack(side="left", padx=5)

    def _validate_number(self, value):
        if value == "":
            return True  # 입력 중 허용
        try:
            float(value)
            return True
        except ValueError:
            return False

