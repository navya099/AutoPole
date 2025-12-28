import tkinter as tk

from ui.taskwizard.taskwizard import TaskWizard
from utils.logger import logger

VERSION = "v1.0.6"

class MainWindow(tk.Tk):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug  # 🔴 debug 인자 저장
        self.title("전주 처리 프로그램")
        self.geometry("500x200")
        self.wizard = None
        # "새 작업" 버튼
        self.new_task_button = tk.Button(self, text="새 작업", command=self.start_wizard)
        self.new_task_button.pack(pady=20)

        # "종료" 버튼
        self.exit_button = tk.Button(self, text="종료", command=self.close_application)
        self.exit_button.pack(pady=20)

        # 버전 정보 라벨
        self.version_label = tk.Label(self, text=f"버전: {VERSION}", fg="gray")
        self.version_label.pack(side="bottom", pady=(10, 5))  # 창 하단에 배치

        logger.info(f'MainWindow 초기화 완료')

    def start_wizard(self):
        """새 작업 마법사 창 시작"""
        self.wizard = TaskWizard(self, debug=self.debug)
        self.wizard.grab_set()  # 메인 창을 잠그고 마법사를 모달 창으로 설정

    def close_application(self):
        """프로그램 종료"""
        self.quit()


