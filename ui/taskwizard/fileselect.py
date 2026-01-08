from ui.taskwizard.steppanels import StepPanel
import tkinter as tk
from tkinter import filedialog
from utils.logger import logger


class FileSelectionPanel(StepPanel):
    def show(self):
        self.clear()
        tk.Label(self.master, text="단계1: 파일 선택", font=("Arial", 14)).pack(pady=10)

        file_titles = [
            'curve_info.txt',
            'pitch_info.txt',
            'bve_coordinates.txt',
            'structures.xlsx'
        ]

        for i, title in enumerate(file_titles):
            frame = tk.Frame(self.master)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{title}:").pack(side="left")

            # ✅ 기존 StringVar 재사용
            var = self.state.file_paths[i]

            entry = tk.Entry(frame, width=40, textvariable=var)
            entry.pack(side="left", padx=5)

            tk.Button(
                frame,
                text="열기",
                command=lambda i=i: self.browse_file(i)
            ).pack(side="left")

    def browse_file(self, i):
        file_path = filedialog.askopenfilename()
        if file_path:
            logger.info(f"파일 선택됨: {file_path}")
            self.state.file_paths[i].set(file_path)
