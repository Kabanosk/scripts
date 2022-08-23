import argparse
from pathlib import Path
import concurrent.futures

from pytube import YouTube
from moviepy.editor import VideoFileClip

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download videos from all urls from file (only youtube urls)")
    parser.add_argument(
        '--urls_file', '-f',
        type=Path,
        help="File with urls (.txt format)"
    )
    parser.add_argument(
        '--url', '-u',
        type=str,
        help="Url address to video which will be downloaded"
    )
    parser.add_argument(
        '--output_dir', '-o',
        type=Path,
        default=Path('.'),
        help="Directory in which videos will be downloaded"
    )
    parser.add_argument(
        '--mp3',
        action='store_true',
        help="Add this argument if you want to download only audio"
    )
    return parser.parse_args()


def check_arguments(file, output_dir):
    assert (
        file is None or file.exists()
    ), f"Path '{file}' not exists"
    assert (
        file is None or file.suffix == '.txt'
    ), f"File '{file}' is in wrong format (must be .txt)"
    if output_dir is not None and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)


def replace_whitespaces(text):
    url = text.replace(' ', '')
    url = url.replace('\n', '')
    url = url.replace('\t', '')
    return url


def download_video(url):
    global mp3, output_path

    yt = YouTube(url)
    filename = yt.title
    max_res = yt.streams.get_highest_resolution().resolution
    min_res = yt.streams.get_lowest_resolution().resolution

    stream = yt.streams.filter(file_extension='mp4').get_by_resolution(min_res if mp3 else max_res)

    video_path = Path(stream.download(output_path))

    if mp3:
        audio_path = video_path.with_suffix('.mp3')

        with VideoFileClip(str(video_path)) as vclip:
            audioclip = vclip.audio
            audioclip.write_audiofile(str(audio_path))
            audioclip.close()
        video_path.unlink()

    return f"\n\t{filename} downloaded"


if __name__ == "__main__":
    args = parse_arguments()
    mp3 = args.mp3
    output_path = args.output_dir

    check_arguments(args.urls_file, args.output_dir)

    if args.url:
        print(download_video(args.url))

    if args.urls_file:
        with open(args.urls_file, 'r') as f:
            urls = [replace_whitespaces(x) for x in f.readlines()]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(download_video, urls)

            for result in results:
                print(result)
