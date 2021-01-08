"""
Reuturns attributes of playlists 
"""
import csv
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
        
            for item in response['items']:
                # publishedAt, title, description, id_ = get_attributes(item)
                publishedAt, title, description, id_ = get_attributes(item)
                duration = cal_duration(id_)
                csv_writer.writerow([publishedAt, title, description, id_, duration])
        
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

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

def get_attributes(item):
    snippet = item['snippet']
    publishedAt = snippet['publishedAt']
    title = snippet['title']
    description = snippet['description']
    id_ = item['id']
    return publishedAt, title, description, id_

def cal_duration(playlist_id):
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

        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

    total_seconds = int(total_seconds)
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    duration = f'{hours}:{minutes}:{seconds}'
    return duration


playlist()