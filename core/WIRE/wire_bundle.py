class WireBundle:
    def __init__(self, index, start_ref, end_ref, track_index):
        self.index = index
        self.track_index = track_index
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.wires = []  # 핵심
