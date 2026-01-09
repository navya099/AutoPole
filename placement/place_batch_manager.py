from config.spandatabase import SpanDatabase
from placement.pole.poleplaceengine import PolePlaceIRBuilder
from placement.wire.wire_ir_builder import WireIRBuilder
from ui.taskwizard.design_context import DesignContext


class PlaceBatchManager:
    def __init__(self, data: DesignContext):
        self.pole_builder = PolePlaceIRBuilder()
        self.spandb = SpanDatabase(data.speed)
        self.wire_builder = WireIRBuilder(self.spandb, data.poledata)
        self.data = data

    def run(self):
        irs = []
        for pole in self.data.poledata.iter_poles():
            irs.extend(self.pole_builder.build(pole))

        # 2. 전선 IR (track별 순회)
        for track_idx in self.data.poledata.track_indices():
            for bundle in self.data.wiredata.iter_bundles():
                irs.extend(
                    self.wire_builder.build(bundle, track_idx)
                )

        self.data.irs = irs