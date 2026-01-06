from core.WIRE.wire_bundle import WireBundle
from core.WIRE.wire_element import WireElement
from core.WIRE.wire_policy import WIRE_POLICY_TABLE


class WireBuilder:
    def build_bundle(self, index, start_ref, end_ref):
        if start_ref.is_last or end_ref is None:
            return None

        policy = WIRE_POLICY_TABLE[start_ref.section_info]
        bundle = WireBundle(index, start_ref, end_ref)

        for wire_type, rule in policy.items():
            count = rule.decide(start_ref, end_ref)
            for i in range(count):
                bundle.wires.append(
                    WireElement(
                        wire_type=wire_type,
                        index=i,
                        start_ref=start_ref,
                        end_ref=end_ref,
                    )
                )
        return bundle
