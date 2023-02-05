class Chord():
    def __init__(self, root, alter, kind) -> None:
        self.root = root
        self.alter = alter
        self.kind = kind

class ChordStructure:
    def __init__(self, songname) -> None:
        self.name = songname
        self.chords = []
        self.signature = []
        self.tempo = []

    def add_accord(self, chord: Chord, bar: int, subdivision: int):
        item = dict()
        item["bar"] = bar
        item["subdivision"] = subdivision
        item["chord"] = chord
        self.chords.append(item)

    def add_signature(self, signature: dict, bar: int):
        if len(self.signature) == 0:
            item = {"bar": bar, "beats": signature["beats"], "beat-type": signature["beat-type"]}
            self.signature.append(item)
        elif not self.signature[-1]["beats"] == signature["beats"] and self.signature[-1]["beat-type"] == signature["beat-type"]:
            item = {"bar": bar, "beats": signature["beats"], "beat-type": signature["beat-type"]}
            self.signature.append(item)  

    def add_tempo(self, tempo: float, bar: int):
        # please use quater standard
        item = {"bar": bar, "tempo": tempo}
        self.tempo.append(item)    