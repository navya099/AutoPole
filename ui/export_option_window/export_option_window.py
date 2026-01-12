import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from engine.bveengine.bveengine import BveEngine
from fileio.exporter.bve_exporter import BVEExporter
from fileio.exporter.dxf_exporter import DxfManager
from fileio.fileloader import BaseFileHandler


class ExportOptionWindow(tk.Toplevel):
    def __init__(self, master, design_context):
        super().__init__(master)
        self.design_context = design_context
        self.title("데이터 내보내기")
        self.geometry("300x300")

        self.exporters = [
            BVEExporter(),
            DxfManager(),
        ]

        self.selected = tk.StringVar(value=self.exporters[0].name)

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="출력 형식 선택", font=("Arial", 12)).pack(pady=10)

        for exp in self.exporters:
            ttk.Radiobutton(
                self,
                text=exp.name,
                value=exp.name,
                variable=self.selected
            ).pack(anchor="w", padx=20)

        ttk.Button(
            self,
            text="내보내기",
            command=self.run
        ).pack(pady=20)

    def run(self):
        name = self.selected.get()
        exporter = next(e for e in self.exporters if e.name == name)

        try:
            # 1️⃣ export → 문자열 생성
            text = exporter.export(self.design_context.irs)

            # 2️⃣ 저장 경로 선택 (UI 책임)
            filecontroller = BaseFileHandler()
            filecontroller.save_file_dialog()
            #저장
            filecontroller.write_to_file(text)
            messagebox.showinfo("완료", f"{name} 내보내기 완료")
            self.destroy()

        except Exception as e:
            messagebox.showerror("오류", str(e))

