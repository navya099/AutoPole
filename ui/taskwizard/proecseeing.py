# processing.py
import tkinter as tk
from tkinter import ttk

from core.maincore.progress_event import ProgressType
from ui.taskwizard.steppanels import StepPanel
from ui.taskwizard.taskworker import TaskWorker
import queue

class ProcessingPanel(StepPanel):
    def __init__(self, master, state, design_context, on_finished):
        super().__init__(master, state)
        self.design_context = design_context
        self.on_finished = on_finished

    def show(self):
        self.clear()
        tk.Label(self.master, text="단계4: 처리 중", font=("Arial", 14)).pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.master, length=400, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(pady=10)

        self.progress_label = tk.Label(self.master, text="대기 중...")
        self.progress_label.pack(pady=5)

        self.start_button = tk.Button(self.master, text="작업 시작", command=self.start_async_processing)
        self.start_button.pack(pady=10)

    def start_async_processing(self):
        self.progress_label.config(text="작업 시작 중...")
        self.progress_var.set(0)

        self.worker_queue = queue.Queue()
        self.worker = TaskWorker(self.state, self.worker_queue, self.design_context)
        self.worker.start()

        self.master.after(100, self.check_thread)

    def check_thread(self):
        try:
            event = self.worker_queue.get_nowait()

            self.progress_var.set(event.percent)
            self.progress_label.config(text=event.message)

            if event.type == ProgressType.ERROR:
                self.start_button.config(state="disabled")
                return

            if event.type == ProgressType.FINISHED:
                self.start_button.config(state="disabled")
                return

            # check_thread 내부
            if event.percent >= 100:
                self.on_finished()
                return

        except queue.Empty:
            pass

        self.master.after(100, self.check_thread)


