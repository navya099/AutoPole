import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from fileio.dataloader import DataBundle
from utils.logger import logger
from core.core import MainProcess
import threading
import queue

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


class TaskWizard(tk.Toplevel):
    def __init__(self, master, debug=False):
        super().__init__(master)
        self.debug = debug  # 🔴 전달받은 debug 저장
        self.progress_bar = None
        self.progress_var = None
        self.queue = None
        self.thread = None
        self.start_button = None
        self.progress_label = None
        self.process_result_label = None
        self.title("새 전주 생성 마법사")
        self.geometry("500x500")
        self.file_paths = [tk.StringVar() for _ in range(4)]
        self.step = 0
        self.mode = tk.StringVar()
        self.inputs = [tk.StringVar() for _ in range(7)]  # 4개의 입력에 대해 StringVar 초기화
        self.next_button = None  # Initialize next_button as None
        self.update_step()
        self.curve_info_path = None
        self.pitch_info_path = None
        self.coord_info_path = None
        self.structure_path = None
        logger.debug("[DEBUG MODE] 디버그 모드로 마법사 시작됨")

    def update_step(self):
        """현재 단계 UI 업데이트"""
        # 기존 위젯 제거
        for widget in self.winfo_children():
            widget.destroy()

        # 각 단계별 UI 구성
        if self.step == 0:
            self.select_file_paths()
            self.enable_next_button(True)

        elif self.step == 1:
            self.select_mode()
        elif self.step == 2:
            self.get_inputs()
            self.enable_next_button(True)  # 유효성 검사 후 '다음' 버튼 활성화
        elif self.step == 3:
            self.process_data()
        elif self.step == 4:
            tk.Label(self, text="마침", font=("Arial", 14)).pack(pady=10)
            tk.Label(self, text="모든 작업이 끝났습니다!", font=("Arial", 12)).pack(pady=10)

        # 버튼 프레임
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        if self.step > 0:
            tk.Button(button_frame, text="이전", command=self.prev_step).pack(side="left", padx=5)

        # '다음' 버튼 초기화
        if self.next_button:
            self.next_button.destroy()  # 이전에 있던 next_button을 제거합니다.

        if self.step < 4:
            self.next_button = tk.Button(button_frame, text="다음", command=self.next_step)
            self.next_button.pack(side="left", padx=5)
        else:
            tk.Button(button_frame, text="완료", command=self.finish_wizard).pack(side="left", padx=5)

        tk.Button(button_frame, text="취소", command=self.cancel).pack(side="right", padx=5)

    def enable_next_button(self, state):
        """'다음' 버튼 활성화/비활성화"""
        if self.next_button and self.next_button.winfo_exists():  # Ensure button exists
            self.next_button.config(state="normal" if state else "disabled")

    def next_step(self):
        """다음 단계로 이동"""
        if self.step == 2:
            if self.validate_inputs():  # 유효성 검사
                self.step += 1
                self.update_step()
            else:
                messagebox.showerror('에러', '입력값에 오류가 있습니다.')
        elif self.step == 4:
            self.finish_wizard()  # 마지막 단계에서는 마법사 완료 처리
            return
        elif self.step == 0:
            if all(path.get() for path in self.file_paths):
                self.step += 1
                self.update_step()
            else:
                logger.error('에러 : 파일이 선택되지 않았습니다.')
                messagebox.showerror('에러', '파일이 선택되지 않았습니다.')
                return
        elif self.step == 1:
            self.step += 1
            self.update_step()

        elif self.step == 3:
            self.step += 1
            self.update_step()

    def prev_step(self):
        """이전 단계로 이동"""
        if self.step > 0:
            self.step -= 1
            self.update_step()

    def cancel(self):
        """마법사 종료"""
        self.destroy()

    def select_file_paths(self):
        """Step 1: 파일 경로 선택"""

        # 항상 초기화
        self.file_paths = [tk.StringVar() for _ in range(4)]

        if self.debug:
            # 디버그 경로 자동 지정
            default_paths = [
                "C:/Temp/curve_info.txt",
                "C:/Temp/pitch_info.txt",
                "C:/Temp/bve_coordinates.txt",
                "C:/Temp/구조물.xlsx"
            ]
            for i in range(4):
                self.file_paths[i].set(default_paths[i])

            self.curve_info_path = self.file_paths[0]
            self.pitch_info_path = self.file_paths[1]
            self.coord_info_path = self.file_paths[2]
            self.structure_path = self.file_paths[3]

            # 디버그 메시지 출력 (UI 위젯은 생략)
            tk.Label(self, text="단계1(디버그 모드): 파일 자동 설정됨", font=("Arial", 14), fg="gray").pack(pady=10)
            logger.debug("DEBUG 모드: 파일 경로 자동 지정 완료")
            return  # UI 생성 생략

        # 일반 모드: 수동 파일 선택 UI
        tk.Label(self, text="단계1: 파일 선택", font=("Arial", 14)).pack(pady=10)

        file_titles = [
            'curve_info.txt',
            'pitch_info.txt',
            'bve_coordinates.txt',
            'structures.xlsx'
        ]

        for i, title in enumerate(file_titles):
            frame = tk.Frame(self)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{title}:").pack(side="left")
            entry = tk.Entry(frame, width=40, textvariable=self.file_paths[i])
            entry.pack(side="left", padx=5)
            button = tk.Button(frame, text="열기", command=lambda i=i: self.browse_file(i))
            button.pack(side="left")

        self.curve_info_path = self.file_paths[0]
        self.pitch_info_path = self.file_paths[1]
        self.coord_info_path = self.file_paths[2]
        self.structure_path = self.file_paths[3]

    def browse_file(self, i):
        """파일 선택 대화상자"""
        file_path = filedialog.askopenfilename()
        if file_path:
            logger.info(f"파일 선택됨: {file_path}")  # 디버깅용 출력
            self.file_paths[i].set(file_path)

    def select_mode(self):
        """Step 2: 모드 선택"""
        tk.Label(self, text="단계 2: 모드 선택", font=("Arial", 14)).pack(pady=10)

        for mode in ['기존 노선용', '새 노선용']:
            tk.Radiobutton(self, text=mode, variable=self.mode, value=mode).pack(pady=5)

    def get_inputs(self):
        """Step 3: 입력값 받기"""
        tk.Label(self, text="Step 3: Enter Details", font=("Arial", 14)).pack(pady=10)

        inputs_text_title = [
            '설계속도',
            '선로 갯수',
            '선로중심간격',
            '폴 방향',
            '시작 측점',
            '끝 측점',
            '파정'
        ]

        # 콤보박스로 대체할 값 목록 (예시)
        combo_options = {
            0: ['150', '250', '350'],  # 설계속도
            3: ['-1', '1'],  # 폴 방향
        }

        for i, label in enumerate(inputs_text_title):
            frame = tk.Frame(self)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{label}:").pack(side="left")

            if i in combo_options:
                combobox = ttk.Combobox(frame, textvariable=self.inputs[i], values=combo_options[i], state="readonly")
                combobox.pack(side="left", padx=5)
                combobox.current(0)  # 기본 선택값 설정
            else:
                entry = tk.Entry(frame, textvariable=self.inputs[i])
                entry.pack(side="left", padx=5)

    def validate_inputs(self):
        """입력값 유효성 검사"""
        for i, input_var in enumerate(self.inputs):
            value = input_var.get().strip()  # 공백 제거

            # 각 입력값에 대해 타입 체크 및 유효성 검사
            if i == 0:  # '설계속도'
                if not value.isdigit():  # 숫자가 아닌 경우
                    messagebox.showerror("입력 오류", "설계속도는 숫자만 입력할 수 있습니다.")
                    return False  # 유효성 검사 실패
                speed = int(value)
                if speed <= 0:
                    messagebox.showerror("입력 오류", "설계속도는 0보다 큰 값이어야 합니다.")
                    return False

                if speed not in [150, 250, 350]:
                    messagebox.showerror("입력 오류", "설계속도는 150, 250, 350 중 하나여야 합니다.")
                    return False
            elif i == 1:  # '선로 갯수'
                if not value.isdigit():
                    messagebox.showerror("입력 오류", "선로 갯수는 숫자만 입력할 수 있습니다.")
                    return False  # 유효성 검사 실패
                if int(value) < 1:  # 1 이상이어야 함
                    messagebox.showerror("입력 오류", "선로 갯수는 최소 1이어야 합니다.")
                    return False  # 유효성 검사 실패

            elif i == 2:  # '선로중심간격'
                try:
                    float_value = float(value)
                except ValueError:  # 숫자가 아닌 경우
                    messagebox.showerror("입력 오류", "선로중심간격은 숫자만 입력할 수 있습니다.")
                    return False  # 유효성 검사 실패
                if float_value <= 0:  # 0 이하일 수 없음
                    messagebox.showerror("입력 오류", "선로중심간격은 0보다 큰 값이어야 합니다.")
                    return False  # 유효성 검사 실패

            elif i == 3:  # '폴 방향'
                if value not in ['-1', '1']:  # 예시로, 방향을 특정 값으로 제한
                    messagebox.showerror("입력 오류", "폴 방향은 -1, 1 중 하나여야 합니다.")
                    return False  # 유효성 검사 실패

        return True  # 모든 검사 통과 시 True 반환

    def process_data(self):
        tk.Label(self, text="Step 4: Processing Data", font=("Arial", 14)).pack(pady=10)

        self.progress_label = tk.Label(self, text="작업 대기 중...", font=("Arial", 12))
        self.progress_label.pack(pady=10)

        # Progressbar 추가
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, maximum=100, length=400, variable=self.progress_var,
                                            mode='determinate')
        self.progress_bar.pack(pady=10)

        self.start_button = tk.Button(self, text="작업 시작", command=self.start_async_processing)
        self.start_button.pack(pady=10)

    def finish_wizard(self):
        """마법사 완료 후 창 닫기"""
        self.destroy()

    def start_async_processing(self):
        self.progress_label.config(text="작업 시작 중...")
        self.progress_var.set(0)
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.run_main_process, args=(self.queue,))
        self.thread.start()
        self.after(100, self.check_thread)

    def run_main_process(self, q):
        try:
            databundle = DataBundle(
                designspeed=int(self.inputs[0].get()),
                linecount=int(self.inputs[1].get()),
                lineoffset=float(self.inputs[2].get()),
                poledirection=int(self.inputs[3].get()),
                mode=0 if self.mode.get() == '기존 노선용' else 1,
                curve_path=self.file_paths[0].get(),
                pitch_path=self.file_paths[1].get(),
                coord_path=self.file_paths[2].get(),
                structure_path=self.file_paths[3].get(),
                start_sta=float(self.inputs[4].get()),
                end_sta=float(self.inputs[5].get()),
                offset=float(self.inputs[6].get())
            )
            process = MainProcess(databundle)
            process.run_with_callback(progress_callback=q.put)
            q.put("100|완료")  # 최종 완료 상태
        except Exception as e:
            logger.error(f"작업 처리 중 오류 발생: {e}", exc_info=True)
            q.put("오류|작업 실패")

    def check_thread(self):
        try:
            message = self.queue.get_nowait()
            if "|" in message:
                percent, text = message.split("|", 1)
                self.progress_var.set(float(percent))
                self.progress_label.config(text=text)
            else:
                self.progress_label.config(text=message)

            if message.endswith("완료") or message.startswith("에러"):
                self.start_button.config(state='disabled')
                return
        except queue.Empty:
            pass
        self.after(100, self.check_thread)
