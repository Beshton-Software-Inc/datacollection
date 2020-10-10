import sys, os, getopt
from youtube_downloader import run_command, make_and_change_directory

def sort_chunked_snippets_into_corpus_dataset(directory, target_directory):
    make_and_change_directory(target_directory)
    make_and_change_directory('../')
    
    count = 0
    for root, _, files in os.walk(directory):
        if 'chunked_snippets' not in root:
            continue
        for name in files:
            if 'audio' not in name:
                continue
            
            split_root = root.split('/')
            if len(split_root) < 5:
                print(f"Root did not have language code in path, skipping: {root}")
                continue
            language_code = split_root[2]
            video_id = split_root[4]
            make_and_change_directory(target_directory + "/" + language_code + "/" + video_id)
            make_and_change_directory('../../..')

            chunk_number = name[6:len(name)-5]
            audio_file_path = os.path.join(root, name)
            transcript_file_path = os.path.join(root, f"transcript_{chunk_number}.txt")
            new_file_path = f"{target_directory}/{language_code}/{video_id}/chunk_{count}"

            run_command(f"cp {audio_file_path} {new_file_path}.flac")
            _, stderr = run_command(f"ffmpeg -loglevel error -hide_banner -i {new_file_path}.flac {new_file_path}.wav")
            if stderr is not None and len(stderr) > 0:
                print(f"Error while attempting to convert flac snippet ({new_file_path}) to wav: {stderr}")
                run_command(f"rm {new_file_path}.wav")
            else:
                run_command(f"rm {new_file_path}.flac")
                run_command(f"cp {transcript_file_path}  {new_file_path}.txt")
            count += 1
    return
    
if __name__ == "__main__":
    directory = None
    target_directory = None
    
    options, _ = getopt.getopt(sys.argv[1:], 'd:t:', ['directory=', 'target_directory='])
    for opt, arg in options:
        if opt in ('-d', '--directory'):
            directory = arg
        if opt in ('t', '--target_directory'):
            target_directory= arg
    sort_chunked_snippets_into_corpus_dataset(directory, target_directory)