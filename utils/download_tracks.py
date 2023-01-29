import youtube_dl
import os
from argparse import ArgumentParser

def youtube_download(video_url: str, filename: str = None, data_root: str = "data"):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    if filename is None:
        filename = f"{video_info['title']}.mp3"
    if not os.path.exists(data_root):
        os.makedirs(data_root)
    destination = os.path.join(data_root, filename)
    options={
        'format':'bestaudio/best',
        'keepvideo': False,
        'outtmpl': destination,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print(f"Download complete... {destination}")

if __name__=="__main__":
    parser = ArgumentParser("Program for downloading samples from You Tube")
    parser.add_argument("link")
    parser.add_argument("--output-dir", help="Output file path", default="data/samples")
    parser.add_argument("--output-file", help="Output file name", default=None)
    args = parser.parse_args()
    youtube_download(args.link, args.output_file, args.output_dir)