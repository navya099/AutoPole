import json

class JsonExporter:
    def poleref_to_dict(self, ref) -> dict:
        return {
            "pos": ref.pos,
            "span": ref.span,
            "curve_type": ref.curve_type,
            "radius": ref.radius,
            "cant": ref.cant,
            "pitch": ref.pitch,
            "structure_type": ref.structure_type,
            "azimuth": ref.azimuth,
            "center_coord": {
                "x": ref.center_coord.x,
                "y": ref.center_coord.y
            }
        }

    def export_polerefdata(self, polerefdatas, path: str):
        data = [self.poleref_to_dict(ref) for ref in polerefdatas]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def mastspec_to_dict(self, spec) -> dict:
        return {
            "index": spec.index,
            "direction": spec.direction.name
        }

    def polegroup_to_dict(self, group) -> dict:
        return {
            "pos": group.pos,
            "poles": {
                str(track): self.pole_to_dict(pole)
                for track, pole in group.poles.items()
            }
        }

    def pole_to_dict(self, pole) -> dict:
        return {
            "track_index": pole.track_index,
            "pos": pole.pos,
            "post_number": pole.post_number,
            "gauge": pole.gauge,
            "span": pole.span,
            "ispreader": pole.ispreader,
            "direction": pole.direction.name,
            "coord": {
                "x": pole.coord.x,
                "y": pole.coord.y
            },
            "current_section": pole.current_section,
            "masts": [
                self.mastspec_to_dict(spec)
                for spec in pole.masts
            ]
        }

    def export_polegroups(self, polegroup_manager, path: str):
        data = [
            self.polegroup_to_dict(group)
            for group in polegroup_manager.groups
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


