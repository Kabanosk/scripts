import argparse
from pathlib import Path
import concurrent.futures

from pytube import YouTube


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download videos from all urls from file (only youtube urls)")
    parser.add_argument(
        '--urls_file', '-f',
        type=Path,
        help="File with urls (.txt format)"
    )
    parser.add_argument(
        '--output_dir', '-o',
        type=Path,
        default=Path('.'),
        help="Directory in which videos will be downloaded"
    )
    parser.add_argument(
        '--url', '-u',
        type=str,
        help="Url address to video which will be downloaded"
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
    yt = YouTube(url)
    res = yt.streams.get_highest_resolution().resolution
    yt.streams\
        .filter(file_extension='mp4')\
        .get_by_resolution(res)\
        .download(output_path)
    return f"Video {yt.title} by {yt.author} downloaded"


if __name__ == "__main__":
    args = parse_arguments()
    global output_path
    output_path = args.output_dir

    check_arguments(args.urls_file, args.output_dir)

    if args.url:
        download_video(args.url)

    if output_path and args.urls_file:
        with open(args.urls_file, 'r') as f:
            urls = [replace_whitespaces(x) for x in f.readlines()]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(download_video, urls)

            for result in results:
                print(result)
