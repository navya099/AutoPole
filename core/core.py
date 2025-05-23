from fileio.dxf_exporter import DxfManager
from .brackets import BracketManager
from .pole import *
from fileio.dataloader import *
from fileio.bve_exporter import *
from .wire import WirePositionManager


class MainProcess:
    def __init__(self, datalbudle: DataBundle):
        self.feedermanager = None
        self.dxfmanager = None
        self.csvmanager = None
        self.wiremanager = None
        self.mastmanager = None
        self.bracket_manager = None
        self.loader = None
        self.pole_processor = None
        self.datalbudle = datalbudle
        self.steps = []

    def run_with_callback(self, progress_callback=None):
        def update(step_idx, msg):
            if progress_callback:
                pct = int((step_idx / total_steps) * 100)
                progress_callback(f"{pct}|🔄 ({step_idx} / {total_steps}) {pct}% - {msg}")

        # 작업 단계 정의
        self.steps = [
            ("📦 데이터 로딩 중...", self.load_data),
            ("📍 전주 배치 계산 중...", self.calc_pole),
            ("🪛 브래킷 설치 중...", self.install_bracket),
            ("🪛 급전선 설치 중...", self.install_feeder),
            ("📐 마스트 배치 중...", self.place_mast),
            ("⚡ 와이어 배선 중...", self.route_wire),
            ("📝 CSV 내보내는 중...", self.export_csv),
            ("📝 도면 내보내는 중...", self.export_dxf)
        ]
        total_steps = len(self.steps)

        try:
            for idx, (msg, func) in enumerate(self.steps):
                update(idx, msg)
                func()
            update(total_steps, "✅ 모든 작업 완료")
        except Exception as ex:
            if progress_callback:
                progress_callback(f"0|에러: {ex}")
                logger.error(f'에러: {ex}')

    # 단계별 처리 함수
    def load_data(self):
        self.loader = DataLoader(self.datalbudle)

    def calc_pole(self):
        self.pole_processor = PolePositionManager(self.loader)
        self.pole_processor.run()

    def install_bracket(self):
        self.bracket_manager = BracketManager(self.loader, self.pole_processor.poledata)
        self.bracket_manager.run()

    def place_mast(self):
        self.mastmanager = MastManager(self.loader, self.pole_processor.poledata)
        self.mastmanager.run()

    def install_feeder(self):
        self.feedermanager = FeederManager(self.loader, self.pole_processor.poledata)
        self.feedermanager.run()

    def route_wire(self):
        self.wiremanager = WirePositionManager(self.loader, self.pole_processor.poledata)
        self.wiremanager.run()

    def export_csv(self):
        self.csvmanager = BVECSV(self.pole_processor.poledata, self.wiremanager.wiredata)
        self.csvmanager.create_pole_csv()
        self.csvmanager.create_csvtotxt()
        self.csvmanager.create_wire_csv()
        self.csvmanager.create_csvtotxt()

    def export_dxf(self):
        self.dxfmanager = DxfManager(self.pole_processor.poledata, self.wiremanager.wiredata)
        self.dxfmanager.run()

