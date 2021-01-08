"""
Reuturns attributes of playlists 
"""
import os.path
import json
import re
from datetime import timedelta
from googleapiclient.discovery import build
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

path = os.path.join(BASE_DIR, 'config.json')

with open(path) as api_file:
    config = json.load(api_file)

youtube = build('youtube', 'v3', developerKey=config['API_KEY'])

playlist_id = 'PLA7ZcagI0frCtT1hzyeG2orZ7ijtxbrYR'
nextPageToken = None

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

while True:
    pl_request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlist_id,
        maxResults = 50,
        pageToken = nextPageToken
        )
    response = pl_request.execute()

    vid_ids = []
    for item in response['items']:
        vid_ids.append(item['contentDetails']['videoId'])
        
    vid_request = youtube.videos().list(
        part = "contentDetails",
        id=','.join(vid_ids)
        )
    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds =  seconds
            ).total_seconds()

        total_seconds += video_seconds

    nextPageToken = response.get('nextPageToken')

    if not nextPageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours}:{minutes}:{seconds}')