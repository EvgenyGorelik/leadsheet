from datahandler.parsers.musicxml import MusicXML

def parse(filename, annotation_type="musicxml"):
    if annotation_type == "musicxml":
        parser = MusicXML()
    return parser.parse(filename)


if __name__=="__main__":
    parse("data\changes\All The Things You Are.musicxml", annotation_type="musicxml")