import sys, os, webvtt, json, getopt
from subprocess import Popen, PIPE
from googleapiclient.discovery import build

def run_command(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def make_and_change_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

def set_up_youtube_service():
    api_key = os.environ['YOUTUBE_GOOGLE_API_KEY']
    return build('youtube', 'v3', developerKey=api_key)

def get_video_language(response):
    if 'items' not in response:
        return
    if len(response['items']) == 0:
        return
    if 'snippet' not in response['items'][0]:
        return
    if 'defaultAudioLanguage' not in response['items'][0]['snippet']:
        return
    return response['items'][0]['snippet']['defaultAudioLanguage']

def get_video_subtitle_status(video_id):
    list_subs_for_video_id_command = f"youtube-dl -j --skip-download --list-subs {video_id}"
    _, err = run_command(list_subs_for_video_id_command)
    no_caption_indicator = 'Couldn\'t find automatic captions'
    no_subtitle_indicator = 'doesn\'t have subtitles'
    if err is None or len(err) == 0:
        return 'subtitle'
    if no_caption_indicator in err and no_subtitle_indicator in err:
        return
    if no_caption_indicator in err:
        return 'subtitle'
    if no_subtitle_indicator in err:
        return 'auto-caption' 

def get_audio_and_transcripts_for_list(youtube_list_id, latest_video_id_already_chunked, fallback_language_code):
    youtube_service = set_up_youtube_service()
    get_video_ids_from_list_command = f"youtube-dl -j --skip-download --flat-playlist {youtube_list_id} | jq -r '.id'"
    output, err = run_command(get_video_ids_from_list_command)
    video_ids_list = output.split()
    if len(video_ids_list) == 0:
        print(f"Failed to grab id's from video list: {err}")
        return
    make_and_change_directory("downloads/" + youtube_list_id)
    did_pass_already_seen_videos = False
    # Reverse list to go through oldest videos first
    for video_id in reversed(video_ids_list):
        if latest_video_id_already_chunked is not None and not did_pass_already_seen_videos:
            if latest_video_id_already_chunked == video_id:
                did_pass_already_seen_videos = True
            continue
        save_audio_and_transcript_for_video(video_id, youtube_service, fallback_language_code)

def save_audio_and_transcript_for_video(video_id, youtube_service, fallback_language_code):
    video_subtitle_status = get_video_subtitle_status(video_id)
    if video_subtitle_status is None:
        print(f"Video: {video_id} has no automatic or manual subtitles")
        return
    request = youtube_service.videos().list(part='snippet', id=video_id)
    response = request.execute()
    default_audio_language = get_video_language(response)
    if default_audio_language is None and fallback_language_code is None:
        print(f"Video: {video_id} has no default audio language - skipping")
        return
    elif default_audio_language is None:
        print(f"Video: {video_id} has no default audio language - using fallback language code: {fallback_language_code}")
        default_audio_language = fallback_language_code
    make_and_change_directory(default_audio_language)
    download_command = f"youtube-dl --extract-audio --audio-format flac --write-auto-sub {video_id}"
    if video_subtitle_status == 'subtitle':
        print(f"Video: {video_id} has manual subtitles. Attempting to save")
        make_and_change_directory(f'manual/{video_id}')
        download_command = f"youtube-dl --extract-audio --audio-format flac --write-sub {video_id}"
    else:
        print(f"Video: {video_id} has automatic subtitles. Attempting to save")
        make_and_change_directory(f'auto/{video_id}')
    _, err = run_command(download_command)
    if err is None or len(err) == 0:
        print(f"Audio and transcript for video {video_id} saved")
    else:
        print(f"Failed to save audio and transcript for video: {err}")
    save_video_data_to_json_file(response)
    chunk_vtt_into_snippets(video_id)
    os.chdir("../../..")
    return

def chunk_vtt_into_snippets(video_id):
    vtt_file = None
    audio_file = None
    for file in os.listdir():
        if file.endswith(".vtt"):
            os.rename(file, "transcript.vtt")
            vtt_file = file
        if file.endswith(".flac"):
            audio_file = os.rename(file, "audio.flac")
            audio_file = file
    if vtt_file is None or audio_file is None:
        print(f"No vtt or flac file generated for video: {video_id}")
        return
    make_and_change_directory('chunked_snippets')
    start_offset_second = 0
    current_fragment_count = 0
    current_fragment_string = ''
    exact_start_offset_string = '0'
    captions = webvtt.read('../transcript.vtt')
    previous_caption = None
    for i, caption in enumerate(captions):
        caption_end_second = get_end_offset_seconds(caption.end)
        split_line_captions = caption.text.strip().splitlines()
        for line in split_line_captions:
            if line != previous_caption:
                current_fragment_string += ' ' + line
                previous_caption = line
        if (caption_end_second - start_offset_second) > 20 or i == len(captions) - 1:
            trim_audio_file(current_fragment_count, exact_start_offset_string, caption.end)
            save_fragment_to_text_file(current_fragment_string, current_fragment_count)
            start_offset_second = caption_end_second
            current_fragment_count += 1
            current_fragment_string = ''
            exact_start_offset_string = caption.end
    make_and_change_directory('../')

def save_video_data_to_json_file(response):
    with open('video_metadata.json', 'w') as metadata_file:
        json.dump(response, metadata_file)

def trim_audio_file(current_fragment_count, start_offset, end_offset):
    _, err = run_command(f"sox ../audio.flac audio_{current_fragment_count}.flac trim {start_offset} ={end_offset}")
    if err is not None and len(err) > 0:
        print(f"Error while trimming audio file from {start_offset} to {end_offset}: {err}")

def save_fragment_to_text_file(fragment, current_fragment_count):
    fragment_text_file = open(f"transcript_{current_fragment_count}.txt", 'w')
    fragment_text_file.write(fragment)
    fragment_text_file.close()

def get_end_offset_seconds(time_string):
    seconds_map = [3600,60,1]
    return sum([a*b for a,b in zip(seconds_map, [int(i) for i in time_string.split('.')[0].split(":")])])

if __name__ == "__main__":
    youtube_list_id = None
    latest_video_id_already_chunked = None
    fallback_language_code = None
    
    options, _ = getopt.getopt(sys.argv[1:], 'i:l:f:', ['list_id=', 'last_video_seen=', 'fallback_language_code='])
    for opt, arg in options:
        if opt in ('-i', '--list_id'):
            youtube_list_id = arg
        if opt in ('-l', '--last_video_seen'):
            latest_video_id_already_chunked = arg
        if opt in ('-f', '--fallback_language_code'):
            fallback_language_code = arg
    get_audio_and_transcripts_for_list(youtube_list_id, latest_video_id_already_chunked, fallback_language_code)


