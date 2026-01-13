from config.spandatabase import SpanDatabase
from engine.interface.irgroup import IRGroup
from engine.interface.irguopkey import IRGroupKey
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
        groups: dict[tuple[int, float], IRGroup] = {}

        # 1️⃣ 전주 기반 그룹 생성 + Pole IR
        groups: dict[IRGroupKey, IRGroup] = {}

        for pole in self.data.poledata.iter_poles():
            key = IRGroupKey(
                track=pole.track_index,
                pos=pole.ref.pos,
                post_number=pole.post_number
            )

            group = IRGroup(key)
            for ir in self.pole_builder.build(pole):
                group.add(ir)

            groups[key] = group

        # 2️⃣ 전선 IR (track별)
        for track_idx in self.data.poledata.track_indices():
            for bundle in self.data.wiredata.iter_bundles():
                key = IRGroupKey(
                    track=track_idx,
                    pos=bundle.start_ref.pos
                )

                group = groups.get(key)
                if group:
                    for ir in self.wire_builder.build(bundle, track_idx):
                        group.add(ir)

        # 3️⃣ 최종 결과
        self.data.irs = list(groups.values())
