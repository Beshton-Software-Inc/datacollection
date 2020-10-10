import sys, os, getopt
from youtube_downloader import run_command
import multiprocessing as mp

language_dictionaries = {'english': 'montreal_forced_aligner_resources/librispeech-lexicon.txt'}
language_codes = {'english': 'en'}

def run_aligner_on_chunks(directory, montreal_forced_aligner_directory, language):
    language_code = language_codes[language]
    video_dirs = []
    for root, dirs, _ in os.walk(directory):
        if f'chunks/{language_code}' not in root:
            continue
        for video_dir in dirs:
            video_dirs.append((root, video_dir))
    aligner_args = [(root, video_dir, montreal_forced_aligner_directory, language, language_dictionaries[language]) for (root, video_dir) in video_dirs]
    with mp.Pool(20) as pool:
        pool.map(call_forced_aligner, aligner_args)

def call_forced_aligner(args):
    root, video_dir, montreal_forced_aligner_directory, language, dictionary = args
    print(f"Running Montreal Forced Aligner on {video_dir}")
    language_code = root.split('/')[1]
    full_video_path = os.path.join(root, video_dir)
    _, stderr = run_command(f'{montreal_forced_aligner_directory}/bin/mfa_align {full_video_path} {dictionary} {language} aligner_outputs/output_{video_dir}')
    if stderr is not None and len(stderr) > 0:
        print(f"Error while attempting to run forced aligner on {video_dir}: {stderr}")
        run_command(f'rm -r aligner_outputs/output_{video_dir}')
        return
    print(f"Running alignment on {video_dir} complete")

    unaligned = ''
    if (os.path.exists(f'aligner_outputs/output_{video_dir}/unaligned.txt')):
        unaligned = open(f'aligner_outputs/output_{video_dir}/unaligned.txt', 'r').read()
    unaligned_video_dir = f'outputs/unaligned/{language_code}/{video_dir}'
    aligned_video_dir = f'outputs/aligned/{language_code}/{video_dir}'

    for _, _, files in os.walk(full_video_path):
        for name in files:
            if '.wav' not in name:
                continue
            prefix = name[0:len(name)-4]
            if prefix in unaligned:
                if not os.path.exists(unaligned_video_dir):
                    os.makedirs(unaligned_video_dir)
                run_command(f'cp {full_video_path}/{prefix}.wav {unaligned_video_dir}')
                run_command(f'cp {full_video_path}/{prefix}.txt {unaligned_video_dir}')
            else:
                if not os.path.exists(aligned_video_dir):
                    os.makedirs(aligned_video_dir)                
                run_command(f'cp {full_video_path}/{prefix}.wav {aligned_video_dir}')
                run_command(f'cp {full_video_path}/{prefix}.txt {aligned_video_dir}')
    run_command(f'rm -r aligner_outputs/output_{video_dir}')
    print(f"Finished copying over aligned and unaligned chunks for {video_dir}")

if __name__ == "__main__":
    directory = None
    mfa_directory = None
    language = None
    
    options, _ = getopt.getopt(sys.argv[1:], 'd:m:l:', ['directory=', 'mfa_directory=', 'language='])
    for opt, arg in options:
        if opt in ('-d', '--directory'):
            directory = arg
        if opt in ('m', '--mfa_directory'):
            mfa_directory= arg
        if opt in ('l', '--language'):
            language = arg
    run_aligner_on_chunks(directory, mfa_directory, language)

        