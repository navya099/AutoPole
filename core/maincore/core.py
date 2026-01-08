from core.maincore.proceess_step import ProcessStep
from core.maincore.progress_event import ProgressEvent, ProgressType
from utils.logger import logger
from fileio.dataloader import DataBundle, DataLoader
from fileio.jsonexporter import JsonExporter
from core.BRACKET.bracket_manager import BracketManager
from core.BRACKET.brackrt_fittings.bracket_fitting_manager import BracketFittingManager
from core.FEEDER.feeder_manager import FeederManager
from core.MAST.mast_manager import MastManager
from core.POLE.pole_place_manger import PolePlaceDATAManager
from core.POLE.pole_positioner import PolePositionManager
from core.WIRE.wire_manager import WireManager


class MainProcess:
    def __init__(self, datalbudle: DataBundle, design_context):
        self.feedermanager = None
        self.dxfmanager = None
        self.csvmanager = None
        self.wiremanager = None
        self.mastmanager = None
        self.bracket_manager = None
        self.loader = None
        self.pole_processor = None
        self.datalbudle = datalbudle
        self.steps: list[ProcessStep] = []
        self.design_context = design_context

    def run_with_callback(self, progress_callback=None):
        self._build_steps()
        total = len(self.steps)

        try:
            for idx, step in enumerate(self.steps, start=1):
                if progress_callback:
                    progress_callback(ProgressEvent(
                        type=ProgressType.UPDATE,
                        message=step.message,
                        percent=int(idx / total * 100),
                        step=idx,
                        total=total
                    ))

                step.action()  # 🔥 실행은 이 한 줄

            if progress_callback:
                progress_callback(ProgressEvent(
                    type=ProgressType.FINISHED,
                    message="✅ 모든 작업 완료",
                    percent=100,
                    step=total,
                    total=total
                ))

        except Exception as ex:
            if progress_callback:
                progress_callback(ProgressEvent(
                    type=ProgressType.ERROR,
                    message=f"❌ 에러: {ex}",
                    percent=0,
                    step=idx,
                    total=total,
                    exception=ex
                ))
            raise

    # 단계별 처리 함수
    def load_data(self):
        self.loader = DataLoader(self.datalbudle)

    def calc_pole(self):
        self.pole_processor = PolePositionManager(self.loader)
        self.pole_processor.run()
        self.design_context.refdata = self.pole_processor.polerefdata

    def place_mast(self):
        self.pole_place_processor = PolePlaceDATAManager(self.loader,self.design_context.refdata)
        self.pole_place_processor.run()
        self.design_context.poledata = self.pole_place_processor.poledatas
        self.mast_processor = MastManager(self.loader, self.design_context.poledata)
        self.mast_processor.run()


    def install_bracket(self):
        self.bracket_manager = BracketManager(self.pole_processor.airjoint_list, self.loader, self.design_context.poledata)
        self.bracket_manager.run()

    def install_bracket_fitting(self):
        fitting_manager = BracketFittingManager()
        fitting_manager.run(self.design_context.poledata)

    def install_feeder(self):
        self.feedermanager = FeederManager(self.loader, self.design_context.poledata)
        self.feedermanager.run()


    def route_wire(self):
        self.wiremanager = WireManager(self.loader, self.design_context.poledata)
        self.wiremanager.run()
        self.design_context.wiredata = self.wiremanager.wiredata

    def _build_steps(self):
        self.steps = [
            ProcessStep("📦 데이터 로딩 중...", self.load_data),
            ProcessStep("📍 전주 배치 계산 중...", self.calc_pole),
            ProcessStep("📐 마스트 배치 중...", self.place_mast),
            ProcessStep("🪛 브래킷 설치 중...", self.install_bracket),
            ProcessStep("🪛 브래킷 부속 설치 중...", self.install_bracket_fitting),
            ProcessStep("🪛 급전선 설비 설치 중...", self.install_feeder),
            ProcessStep("⚡ 와이어 배선 중...", self.route_wire),
        ]
