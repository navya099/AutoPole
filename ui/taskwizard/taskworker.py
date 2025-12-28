# taskworker.py
import threading
import queue
from utils.logger import logger
from core.core import MainProcess
from fileio.dataloader import DataBundle
from ui.taskwizard.wizardstate import WizardState

class TaskWorker(threading.Thread):
    def __init__(self, state: WizardState, progress_queue: queue.Queue):
        super().__init__()
        self.state = state
        self.queue = progress_queue

    def run(self):
        try:
            databundle = DataBundle(
                designspeed=int(self.state.inputs[0].get()),
                linecount=int(self.state.inputs[1].get()),
                lineoffset=float(self.state.inputs[2].get()),
                poledirection=int(self.state.inputs[3].get()),
                mode=0 if self.state.mode.get() == '기존 노선용' else 1,
                curve_path=self.state.file_paths[0].get(),
                pitch_path=self.state.file_paths[1].get(),
                coord_path=self.state.file_paths[2].get(),
                structure_path=self.state.file_paths[3].get()
            )
            process = MainProcess(databundle)
            process.run_with_callback(progress_callback=self.queue.put)
            self.queue.put("100|완료")
        except Exception as e:
            logger.error(f"작업 처리 중 오류 발생: {e}", exc_info=True)
            self.queue.put("오류|작업 실패")
