import tkinter as tk
from tkinter import ttk

from fileio.exporter.excel_exporter import ExcelExporter
from utils.util import treeview_to_dict
from visualizing.poleplotter import PolePlotter


class ResultWindow(tk.Toplevel):
    def __init__(self, master, design_context):
        super().__init__(master)
        self.design_context = design_context
        self.selected_pole = None

        self.title("설계 결과 요약")
        self.geometry("700x700")
        self.resizable(True, True)

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        # 요약 Treeview
        summary_frame = ttk.LabelFrame(container, text="전주 요약")
        summary_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.columns = ("전주번호","트랙","측점","X","Y","구간","구조물","선형")
        self.tree_summary = self._create_treeview(summary_frame, self.columns)
        self.tree_summary.pack(fill="both", expand=True)
        self._populate_summary()
        self.tree_summary.bind("<<TreeviewSelect>>", self._on_pole_selected)

        # Plotter (재사용)
        self.plot_frame = ttk.LabelFrame(container, text="전주 배치 시각화")
        self.plot_frame.pack(side="right", fill="both", expand=True)
        self.plotter = PolePlotter(self.plot_frame)

        # 상세보기 Treeview
        detail_frame = ttk.LabelFrame(container, text="선택 전주 상세")
        detail_frame.pack(fill="both", expand=True, pady=(0, 10))
        detail_columns = ("종류","이름","인덱스","추가정보")
        self.tree_detail = self._create_treeview(detail_frame, detail_columns, col_width=120)
        self.tree_detail.pack(fill="both", expand=True)

        # 버튼 영역
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="상세보기 초기화", command=self._clear_detail).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="출력", command=self._export).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="닫기", command=self.destroy).pack(side="right")

    def _create_treeview(self, parent, columns, col_width=100):
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=col_width, anchor="center")
        return tree

    def _populate_summary(self):
        for pole in self.design_context.poledata.iter_poles():
            self.tree_summary.insert("", "end", iid=id(pole), values=(
                pole.post_number, pole.track_index, pole.pos,
                getattr(pole.coord,"x",0), getattr(pole.coord,"y",0),
                getattr(pole.current_section,"name",""),
                pole.ref.structure_type, pole.ref.curve_type
            ))

    def _on_pole_selected(self, event):
        selected_id = self.tree_summary.selection()
        if not selected_id: return
        self.selected_pole = self._find_pole_by_id(int(selected_id[0]))
        if self.selected_pole:
            self._populate_detail(self.selected_pole)
            self.plotter.draw_single_pole(self.selected_pole)

    def _find_pole_by_id(self, pole_id):
        for pole in self.design_context.poledata.iter_poles():
            if id(pole) == pole_id: return pole
        return None

    def _populate_detail(self, pole):
        self._clear_detail()
        self._insert_detail_items(getattr(pole,"masts",[]),"Mast","name","code")
        self._insert_detail_items(getattr(pole,"brackets",[]),"Bracket","name","index")
        self._insert_detail_items(getattr(pole,"feeders",[]),"Feeder","name","code")

    def _insert_detail_items(self, items, kind, name_attr, code_attr):
        for item in items:
            self.tree_detail.insert("", "end", values=(
                kind, getattr(item,name_attr,""), getattr(item,code_attr,""), ""
            ))

    def _clear_detail(self):
        for item in self.tree_detail.get_children():
            self.tree_detail.delete(item)

    def _export(self):
        data = treeview_to_dict(self.tree_summary, self.columns)
        ExcelExporter(data, self.columns).export()


