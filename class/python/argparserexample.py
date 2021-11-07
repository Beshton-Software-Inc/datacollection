import os
import argparse
import fnmatch 
import datetime
from time import strftime
from time import gmtime

import multiprocessing as mp 

def get_duration_str(duration):
    hour = int(duration // 3600)
    duration %= 3600
    minutes = int(duration // 60)
    duration %= 60
    seconds = duration

    # duration_str = str(datetime.timedelta(seconds=duration))
    duration_str = f'{hour}:{minutes}:{seconds}'
    return duration_str


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Count audio duration')
    parser.add_argument('--folder', help='folder with audio files', type=str, required=True)
    parser.add_argument('--num_processes', help='number of parallel process', type=int, default=1)
    parser.add_argument('--ext', help='audio file extension', type=str, default='flac')
    parser.add_argument('--filter', help='audio file extension', type=str, default=None)
    args = parser.parse_args()

    files = []
    if os.path.isfile(args.folder):
        files.append(args.folder)
    else:
        for root, dirnames, filenames in os.walk(args.folder):
            for filename in fnmatch.filter(filenames, f'*.{args.ext}'):
                full_filename = os.path.join(root, filename)
                if args.filter is None or args.filter in full_filename:
                    files.append(full_filename)
                    
    print (args.folder)
