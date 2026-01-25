import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PolePlotter:
    """전주 배치 시각화 전담 클래스"""

    def __init__(self, master_frame):
        # Matplotlib Figure 생성
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _setup_plot(self, title="전주 시각화"):
        """공통 플롯 설정"""
        self.ax.clear()
        self.ax.set_title(title)
        self.ax.set_xlabel("X 좌표")
        self.ax.set_ylabel("Y 좌표")
        self.ax.grid(True)

    def draw_all_poles(self, poles):
        """전체 전주 배치 시각화"""
        if not poles:
            return
        xs = [getattr(p.coord, "x", 0) for p in poles]
        ys = [getattr(p.coord, "y", 0) for p in poles]

        self._setup_plot("전체 전주 배치")
        self.ax.plot(xs, ys, marker="o", color="blue", linestyle="-")
        self.canvas.draw()

    def draw_single_pole(self, pole):
        """선택 전주만 강조"""
        if not pole:
            return
        x, y = getattr(pole.coord, "x", 0), getattr(pole.coord, "y", 0)

        self._setup_plot("선택 전주 강조")
        self.ax.plot(x, y, marker="o", color="red", markersize=10)
        self.canvas.draw()