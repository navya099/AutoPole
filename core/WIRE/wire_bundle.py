class WireBundle:
    def __init__(self, index, start_ref, end_ref):
        self.index = index
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.wires = []  # 핵심
