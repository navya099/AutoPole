from ui.taskwizard.steppanels import StepPanel
import tkinter as tk
from tkinter import filedialog
from utils.logger import logger

class FileSelectionPanel(StepPanel):
    def show(self):
        self.clear()
        tk.Label(self.master, text="단계1: 파일 선택", font=("Arial", 14)).pack(pady=10)
        self.entries = []
        file_titles = ['curve_info.txt', 'pitch_info.txt', 'bve_coordinates.txt', 'structures.xlsx']
        for i, title in enumerate(file_titles):
            frame = tk.Frame(self.master)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{title}:").pack(side="left")
            var = tk.StringVar(value=self.state.file_paths[i])
            self.state.file_paths[i] = var
            entry = tk.Entry(frame, width=40, textvariable=var)
            entry.pack(side="left", padx=5)
            tk.Button(frame, text="열기", command=lambda i=i: self.browse_file(i)).pack(side="left")
            self.entries.append(entry)

    def browse_file(self, i):
        """파일 선택 대화상자"""
        file_path = filedialog.askopenfilename()
        if file_path:
            logger.info(f"파일 선택됨: {file_path}")  # 디버깅용 출력
            self.state.file_paths[i].set(file_path)