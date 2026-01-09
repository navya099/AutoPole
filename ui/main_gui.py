import tkinter as tk
from tkinter import messagebox

from ui.export_option_window.export_option_window import ExportOptionWindow
from ui.observer import ResultSubject
from ui.placement_build_ui.placement_builde_windows import PlacementBuildeWindow
from ui.result_windows.result_windo import ResultWindow
from ui.taskwizard.taskwizard import TaskWizard
from utils.logger import logger

VERSION = "v1.0.6"

class MainWindow(tk.Tk):
    def __init__(self, debug=False):
        super().__init__()
        self.result = None
        self.debug = debug  # 🔴 debug 인자 저장
        self.subject = ResultSubject()
        self.subject.attach(self)  # Observer 등록
        self.title("전주 처리 프로그램")
        self.geometry("500x200")
        self.wizard = None

        # 버전 정보 라벨
        self.version_label = tk.Label(self, text=f"버전: {VERSION}\n made by dger", fg="gray")
        self.version_label.pack(side="bottom", pady=(10, 5))  # 창 하단에 배치

        #버튼 프레임
        brn_frame = tk.Frame(self)
        brn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        #버튼 내부 프레임 영역
        inner_frame = tk.Frame(brn_frame)
        inner_frame.pack()  # 기본 pack: 중앙

        #버튼들
        tk.Button(inner_frame, text="새 작업", command=self.start_wizard).pack(side="left", padx=10)

        self.showbutton = tk.Button(inner_frame, text="결과 보기", command=self.show_data)
        self.showbutton.pack(side="left", padx=10)

        self.databutton = tk.Button(inner_frame, text="데이터 생성", command=self.build_data)
        self.databutton.pack(side="left", padx=10)

        self.printbutton = tk.Button(inner_frame, text="출력", command=self.print_data)
        self.printbutton.pack(side="left", padx=10)

        self.resetbutton = tk.Button(inner_frame, text="초기화", command=self.reset)
        self.resetbutton.pack(side="left", padx=10)

        tk.Button(inner_frame, text="종료", command=self.close_application).pack(side="left", padx=10)
        logger.info(f'MainWindow 초기화 완료')

        self.update_buttons()

    def update(self, result):
        """Observer 인터페이스: Subject가 호출"""
        self.update_buttons()

    def update_buttons(self):
        state = "normal" if self.subject.result else "disabled"
        for btn in [self.showbutton, self.databutton, self.printbutton]:
            btn.config(state=state)

    # ------------------------------
    # 버튼 기능
    # ------------------------------
    def start_wizard(self):
        self.wizard = TaskWizard(self, self.subject)
        self.wizard.grab_set() #모달로 메인GUI 잠금

    def show_data(self):
        if self.subject.result:
            ResultWindow(self, self.subject.result)
        else:
            messagebox.showinfo('알림', '설계가 된 값이 없습니다.')
    def build_data(self):
        if self.subject.result:
            PlacementBuildeWindow(self, self.subject.result)
        else:
            messagebox.showinfo('알림', '설계가 된 값이 없습니다.')
    def print_data(self):
        if self.subject.result:
            ExportOptionWindow(self, self.subject.result)
        else:
            messagebox.showinfo('알림', '설계가 된 값이 없습니다.')
    def close_application(self):
        self.quit()

    def reset(self):
        self.subject.result = None
