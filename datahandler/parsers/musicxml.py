from datahandler.parsers.annotations import Chord, ChordStructure
from xml.etree import ElementTree
import os

class MusicXML:
    def __init__(self) -> None:
        
        self.subdivision_parser = {
            "whole": 4,
            "half": 2,
            "quater": 1
        }

    def parse(self, filename):
        tree = ElementTree.parse(filename)
        measures = tree.find("part").findall("measure")
        annotations = ChordStructure(os.path.basename(filename))
        for measure in measures:
            harmony = measure.findall("harmony")
            note = measure.findall("note")
            signature = {"beats": measure.find("attributes").find("time").find("beats").text, "beat-type": measure.find("attributes").find("time").find("beat-type").text}
            bar = measure.attrib["number"]
            quarter = 0
            annotations.add_signature(signature, bar)
            for (h,n) in zip(harmony, note):
                accord = Chord(
                    h.find("root").find("root-step").text,
                    h.find("root").find("root-alter").text,
                    h.find("kind").text)
                annotations.add_accord(accord, bar, quarter)
                quarter += self.subdivision_parser[n.find("type").text]
        return annotations