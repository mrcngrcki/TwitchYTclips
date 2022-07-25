import json
import os
from collections import namedtuple
import string
import requests

# get secrets from json file
with open('twitch_secrets.json', 'r') as openfile:
    twitch_secrets = json.load(openfile)

API_TOKEN = twitch_secrets['api_token']
CLIENT_ID = twitch_secrets['client_id']
HEADERS = {"Authorization": f"Bearer {API_TOKEN}",
           "Client-Id": CLIENT_ID}


def get_streamers_data(json_path: str) -> list:
    """Reads Twitch IDs from JSON file"""
    print('Reading streamers data from file')
    with open(json_path, 'r') as file:
        json_object = json.load(file)

    streamers = json_object['streamer']
    return streamers


def uniquify(path):
    """Adds number if file with the same name is already downloaded"""
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def get_top_clips(streamers: list, date_to_check: str, top_clips_amount: int) -> list:
    """Requests API for data, sorts by views and returns top x clips"""
    all_clips = []
    print("Reading clips data")
    for streamer in streamers:
        response = requests.get(url=f"https://api.twitch.tv/helix/clips?broadcaster_id={streamer['twitch_id']}"
                                    f"&started_at={date_to_check}", headers=HEADERS)
        response_json = json.loads(response.content)
        clips = response_json['data']
        all_clips.append(clips)

    print('Sorting most popular clips')
    all_clips = [x for xs in all_clips for x in xs]
    all_clips.sort(key=lambda x: x["view_count"], reverse=True)
    best_clips = all_clips[:top_clips_amount]
    return best_clips


def download_clips(download_path: str, best_clips: list):
    """Downloads most popular clips"""
    videos = []
    print('Downloading clips')
    for clip in best_clips:
        clip = namedtuple("ObjectName", clip.keys())(*clip.values())
        print(clip.view_count)
        print(f'{clip.broadcaster_name} - {clip.title}')
        preview_index = clip.thumbnail_url.index("-preview")
        video_url = clip.thumbnail_url[:preview_index] + ".mp4"
        print(video_url)
        video = requests.get(url=video_url)

        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        video_path = os.path.normpath(os.path.join(download_path,
                                                   ''.join(
                                                       char for char in clip.title if char in valid_chars) + ".mp4"))

        video_path = uniquify(video_path)

        # download file
        # open(video_path, "wb").write(video.content)
        with open(video_path, "wb") as vid:
            vid.write(video.content)
        videos.append((clip, video_path))
    return videos


def delete_clips(download_path: str):
    """Deletes clips after uploading"""
    print('Deleting clips')
    for file in os.listdir(download_path):
        os.remove(os.path.join(download_path, file))
