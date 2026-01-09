import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

class PlacementBuildeWindow(tk.Toplevel):
    def __init__(self, master, design_context):
        super().__init__(master)
        self.design_context = design_context
        self.title("데이터 생성")
        self.geometry("300x300")
        self.resizable(True, True)

    def run(self):
        pass