from core.WIRE.wire_builder import WireBuilder
from core.WIRE.wiredata_manager import WireDataManager
from core.base_manager import BaseManager
from utils.logger import logger

class WireManager(BaseManager):

    def __init__(self, dataloader, polecollection):
        super().__init__(dataloader)
        self.collection = polecollection
        self.wiredata = WireDataManager()

        logger.debug(f"WireManager 초기화 완료")
    def run(self):
        builder = WireBuilder()

        for track_idx in self.collection.track_indices():
            poles = self.collection.get_poles_by_track(track_idx)

            for i in range(len(poles) - 1):
                start_pole = poles[i]
                end_pole = poles[i + 1]

                bundle = builder.build_bundle(
                    index=i,
                    start_ref=start_pole.ref,
                    end_ref=end_pole.ref,
                )

                if bundle:
                    self.wiredata.bundles.append(bundle)

        logger.info(f"Wire 생성 완료 {len(self.wiredata.bundles)}")