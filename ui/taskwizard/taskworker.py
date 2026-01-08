# taskworker.py
import threading
import queue

from ui.taskwizard.design_context import DesignContext
from utils.logger import logger
from core.maincore.core import MainProcess
from fileio.dataloader import DataBundle
from ui.taskwizard.wizardstate import WizardState

class TaskWorker(threading.Thread):
    def __init__(self, state: WizardState, progress_queue: queue.Queue, design_context: DesignContext):
        super().__init__()
        self.state = state
        self.queue = progress_queue
        self.design_context = design_context
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
            process = MainProcess(databundle, self.design_context)
            process.run_with_callback(progress_callback=self.queue.put)
        except Exception as e:
            logger.error(f"작업 처리 중 오류 발생: {e}", exc_info=True)

