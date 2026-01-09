import tkinter as tk

class ExportOptionWindow(tk.Toplevel):
    def __init__(self, master, design_context):
        super().__init__(master)
        self.design_context = design_context
        self.title("데이터 내보내기")
        self.geometry("300x300")
        self.resizable(True, True)

    def run(self):
        pass
