"""
BVE 자동 전주 설계 프로그램
Made by dger

📌 Ver 1.0.5

✅ 기능 요약:
- 측점 기반 랜덤 전주 자동 배치
- BVE용 CSV 출력 (전주, 전차선 포함)
- 전차선 평면도 DXF 도면 자동 생성
"""

from ui.main_gui import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
