"""
Reuturns attributes of a channels playlists: 

publishedAt, title, description, id_, duration
"""
import csv
import os.path
import json
import re
import time
from tqdm import tqdm
from datetime import timedelta
from googleapiclient.discovery import build
from pathlib import Path

start = time.time()

BASE_DIR = Path(__file__).resolve().parent

path = os.path.join(BASE_DIR, 'config.json')

with open(path) as api_file:
    config = json.load(api_file)

youtube = build('youtube', 'v3', developerKey=config['API_KEY'])

channel_id = 'UChh-akEbUM8_6ghGVnJd6cQ'

filename = 'data/bwf_playlists2.csv'

def playlist():
    """Creates csv file with playlist attributes"""
    write_header()
    nextPageToken=None
    while True:
        response = request_playlist(nextPageToken)

        with open(filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
        
            for item in tqdm(response['items']):
                publishedAt, title, description, id_ = get_attributes(item)
                duration = cal_duration(id_)
                csv_writer.writerow([publishedAt, title, description, id_, duration])
        
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

def cal_duration(playlist_id):
    
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    nextPageToken = None
    while True:
        pl_response = request_playlistitems(playlist_id, nextPageToken)
        vid_response = request_videos(pl_response)
        total_seconds = cal_seconds(vid_response, hours_pattern, minutes_pattern, seconds_pattern)

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break
    duration = convert_seconds(total_seconds)
    return duration

def cal_seconds(vid_response, hours_pattern, minutes_pattern, seconds_pattern):
    total_seconds = 0
    for item in vid_response['items']:
        total = item['contentDetails']['duration']
        hours = hours_pattern.search(total)
        minutes = minutes_pattern.search(total)
        seconds = seconds_pattern.search(total)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds =  seconds
            ).total_seconds()

        total_seconds += video_seconds
    return total_seconds

def convert_seconds(total_seconds):
    total_seconds = int(total_seconds)
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    duration = f'{hours}:{minutes}:{seconds}'
    return duration

def write_header():

    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['publishedAt', 'title', 'description', 'id', 'duration'])

def request_playlist(nextPageToken):

    request = youtube.playlists().list(
        part = 'contentDetails, snippet',
        channelId = channel_id,
        maxResults = 50,
        pageToken = nextPageToken
        )
    response = request.execute()
    return response

def request_playlistitems(playlist_id, nextPageToken):
    request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlist_id,
        maxResults = 50,
        pageToken = nextPageToken
        )
    response = request.execute()
    return response

def request_videos(pl_response):
    vid_ids = []
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])
        
    vid_request = youtube.videos().list(
        part = "contentDetails",
        id=','.join(vid_ids)
        )
    vid_response = vid_request.execute()
    return vid_response

def get_attributes(item):

    snippet = item['snippet']
    publishedAt = snippet['publishedAt']
    title = snippet['title']
    description = snippet['description']
    id_ = item['id']
    return publishedAt, title, description, id_

playlist()

finish = time.time()
secs = round((finish - start), 2)
print(f"\nTotal time taken {secs}s.")