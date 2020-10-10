import sys, os, getopt
from youtube_downloader import run_command

# audio_type Options
# original_downloaded - get the length original chunked up audio from youtube_downloader
def get_total_length_of_downloaded_audio(directory, audio_type):
    total = 0
    for root, _, files in os.walk(directory):
        if audio_type == 'original_downloaded' and 'chunked_snippets' in root:
            continue
        for name in files:
            if name == 'audio.flac' or name.split(".")[-1] == 'wav':
                stdout, stderr = run_command(f"soxi -D {os.path.join(root, name)}")
                if stderr is not None and len(stderr) > 0:
                    print(f"Error while attempting to grab length of audio clip, {os.path.join(root, name)}: {stderr}")
                    continue
                total += float(stdout)
    print(total)

if __name__ == "__main__":
    directory = None
    chunk_type = None
    
    options, _ = getopt.getopt(sys.argv[1:], 'd:c:', ['directory=', 'chunk_type='])
    for opt, arg in options:
        if opt in ('-d', '--directory'):
            directory = arg
        if opt in ('-c', '--chunk_type'):
            chunk_type = arg
    get_total_length_of_downloaded_audio(directory, chunk_type)