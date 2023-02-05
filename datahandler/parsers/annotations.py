def encode_chordname(root, alter=None):
    encoding = {
        "C": 0,
        "C#": 1,
        "Db": 1,
        "Db": 1,
        "D": 2,
        "D#": 3,
        "Eb": 3,
        "E": 4,
        "E#": 5,
        "F": 5,
        "F#": 6,
        "Gb": 6,
        "G": 7,
        "G#": 8,
        "Ab": 8,
        "A": 9,
        "A#": 10,
        "Bb": 10,
        "B": 11,
    }
    if alter is not None:
        if alter == 1:
            root += "#"
        elif alter == -1:
            root += "b"
    return encoding[root]

def encode_alteration(kind, extension):
    kind_encoding = {
        ""      :   1,
        "major" :   1,
        "m"     :   -1,
        "minor" :   -1,
        "-"     :   -1
    }
    extension = {
        "7"         : 0,
        "min7"    : 0,
        "minor7"    : 0,
        "minor-7"   : 0,
        "b7"        : 0,
        "major7"    : 1,
        "maj7"      : 1,
    }


class Chord():
    def __init__(self, root, alter = None, kind = None, extension = None) -> None:
        self.root = encode_chordname(root, alter)
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