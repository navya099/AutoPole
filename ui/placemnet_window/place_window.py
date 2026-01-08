import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PlaceWindow(tk.Toplevel):
    """설계 결과 요약 및 전주 상세보기"""

    def __init__(self, master, design_context, on_export=None):
        super().__init__(master)
        self.design_context = design_context
        self.on_export = on_export

        self.title("설계 결과 요약")
        self.geometry("700x700")
        self.resizable(True, True)

        self.selected_pole = None

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        # -----------------------------
        # 요약 Treeview
        # -----------------------------
        summary_frame = ttk.LabelFrame(container, text="전주 요약")
        summary_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("전주번호", "트랙", "측점", "X", "Y", "구간")  # 예시로 열 추가
        self.tree_summary = ttk.Treeview(
            summary_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # 헤더 설정
        for col in columns:
            self.tree_summary.heading(col, text=col)
            self.tree_summary.column(col, width=100, anchor="center")

        # 세로 스크롤바
        vsb = ttk.Scrollbar(summary_frame, orient="vertical", command=self.tree_summary.yview)
        vsb.pack(side="right", fill="y")
        self.tree_summary.configure(yscrollcommand=vsb.set)

        # ✅ 가로 스크롤바
        hsb = ttk.Scrollbar(summary_frame, orient="horizontal", command=self.tree_summary.xview)
        hsb.pack(side="bottom", fill="x")
        self.tree_summary.configure(xscrollcommand=hsb.set)

        self.tree_summary.pack(fill="both", expand=True)

        # 전주 데이터 로드
        self._populate_summary()

        # 선택 이벤트
        self.tree_summary.bind("<<TreeviewSelect>>", self._on_pole_selected)

        # -----------------------------
        # 상세보기 Treeview
        # -----------------------------
        detail_frame = ttk.LabelFrame(container, text="선택 전주 상세")
        detail_frame.pack(fill="both", expand=True, pady=(0, 10))

        detail_columns = ("종류", "이름", "인덱스", "추가정보")
        self.tree_detail = ttk.Treeview(detail_frame, columns=detail_columns, show="headings")
        for col in detail_columns:
            self.tree_detail.heading(col, text=col)
            self.tree_detail.column(col, width=120, anchor="center")
        self.tree_detail.pack(fill="both", expand=True)

        # -----------------------------
        # 버튼 영역
        # -----------------------------
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="상세보기 초기화", command=self._clear_detail).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="출력", command=self._export).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="닫기", command=self.destroy).pack(side="right")

    def _populate_summary(self):
        """요약 Treeview 데이터 채우기"""
        for pole in self.design_context.poledata.iter_poles():
            self.tree_summary.insert(
                "",
                "end",
                iid=id(pole),
                values=(
                    pole.post_number,
                    pole.track_index,
                    pole.pos,
                    getattr(pole.coord, "x", 0),
                    getattr(pole.coord, "y", 0),
                    getattr(pole.current_section, "name", ""),
                )
            )

    def _on_pole_selected(self, event):
        """요약 Treeview에서 전주 선택 시 상세보기"""
        selected_id = self.tree_summary.selection()
        if not selected_id:
            return
        pole_obj_id = selected_id[0]

        # 선택 전주 객체
        self.selected_pole = None
        for pole in self.design_context.poledata.iter_poles():
            if id(pole) == int(pole_obj_id):
                self.selected_pole = pole
                break

        if self.selected_pole:
            self._populate_detail(self.selected_pole)

    def _populate_detail(self, pole):
        """상세보기 Treeview 데이터 채우기"""
        self._clear_detail()

        # Mast
        for mast in getattr(pole, "masts", []):
            self.tree_detail.insert("", "end", values=("Mast", getattr(mast, "name", ""), getattr(mast, "code", ""), ""))

        # Bracket
        for bracket in getattr(pole, "brackets", []):
            self.tree_detail.insert("", "end", values=("Bracket", getattr(bracket, "name", ""), getattr(bracket, "index", ""), ""))

        # Feeder
        for feeder in getattr(pole, "feeders", []):
            self.tree_detail.insert("", "end", values=("Feeder", getattr(feeder, "name", ""), getattr(feeder, "code", ""), ""))

    def _clear_detail(self):
        """상세보기 초기화"""
        for item in self.tree_detail.get_children():
            self.tree_detail.delete(item)

    def _export(self):
        """출력 버튼"""
        if self.on_export:
            self.on_export()
        else:
            messagebox.showinfo("알림", "출력 기능은 구현되지 않았습니다.")
