class WireCountRule:
    def __init__(self, min_count, max_count):
        self.min_count = min_count
        self.max_count = max_count

    def decide(self, start_ref, end_ref):
        if self.min_count == self.max_count:
            return self.min_count

        if start_ref.structure_type == "ISLAND_PLATFORM":
            return self.max_count

        return self.min_count
