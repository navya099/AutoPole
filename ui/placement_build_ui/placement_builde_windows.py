import tkinter as tk
from tkinter import ttk

from placement.place_batch_manager import PlaceBatchManager


class PlacementBuildeWindow(tk.Toplevel):
    def __init__(self, master, design_context):
        super().__init__(master)
        self.design_context = design_context
        self.title("데이터 생성")
        self.geometry("300x300")
        self.resizable(True, True)

        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)
        # 버튼 영역
        # -----------------------------
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill="x")

        self.commitbutton = ttk.Button(btn_frame, text="생성", command=self.run)
        self.commitbutton.pack(side="left", padx=5)

        self.exit = ttk.Button(btn_frame, text="닫기", command=self.destroy)
        self.exit.pack(side="left", padx=5)

        #체크박스
        chk_frame = ttk.Frame(self, padding=10)
        chk_frame.pack(fill="x")

        self.range_chk_var = tk.IntVar()
        self.range_chk_box = ttk.Checkbutton(chk_frame, variable=self.range_chk_var)
        self.range_chk_box.pack(side="left", padx=5)

    def run(self):
        ir = PlaceBatchManager(self.design_context)
        ir.run()