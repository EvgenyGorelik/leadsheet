from datahandler.parsers.annotations import Chord, ChordStructure
import json
import os

class MusicJSON:
    def __init__(self) -> None:
        self.subdivision_parser = {
            "whole": 4,
            "half": 2,
            "quater": 1
        }

    def parse(self, filename):
        measures = json.load(filename)
        annotations = ChordStructure(os.path.basename(filename))
        for measure in measures:
            signature = {"beats": measure["beats"], "beat-type": measure["beat-types"]}
            bar = measure["bar"]
            quarter = 0
            annotations.add_signature(signature, bar)
            for chord in measure["changes"]:
                annotations.add_accord(Chord(
                    chord["chord"],
                    chord["chord-type"],
                    chord["chord-alteration"]), bar, quarter)
                quarter += chord["duration"]
        return annotations