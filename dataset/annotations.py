from xml.etree import ElementTree
import os

class Annotation():
    def __init__(self, root, alter, kind) -> None:
        self.root = root
        self.alter = alter
        self.kind = kind

class AnnotationList:
    def __init__(self, songname) -> None:
        self.name = songname
        self.chords = []

    def add_accord(self, chord: Annotation, bar: int, quarter: int):
        item = dict()
        item["bar"] = bar
        item["quarter"] = quarter
        item["chord"] = chord
        self.chords.append(item)

        

TXT_TO_QUARTER = {
    "whole": 4,
    "half": 2
}

def load_annotations(filename):
    tree = ElementTree.parse(filename)
    measures = tree.find("part").findall("measure")
    annotations = AnnotationList(os.path.basename(filename))
    for measure in measures:
        harmony = measure.findall("harmony")
        note = measure.findall("note")
        bar = measure.attrib["number"]
        quarter = 0
        for (h,n) in zip(harmony, note):
            accord = Annotation(
                h.find("root").find("root-step").text,
                h.find("root").find("root-alter").text,
                h.find("kind").text)
            annotations.add_accord(accord, bar, quarter)
            quarter += TXT_TO_QUARTER[n.find("type").text]
    return annotations


if __name__=="__main__":
    load_annotations("data\changes\All The Things You Are.musicxml")