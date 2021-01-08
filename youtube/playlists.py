"""
Reuturns attributes of playlists 
"""
import csv
import os.path
import json
from googleapiclient.discovery import build
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

path = os.path.join(BASE_DIR, 'config.json')

with open(path) as api_file:
    config = json.load(api_file)

youtube = build('youtube', 'v3', developerKey=config['API_KEY'])

channel_id = 'UChh-akEbUM8_6ghGVnJd6cQ'

filename = 'data/bwf_playlists.csv'



def playlist():
    """Creates csv file with playlist attributes"""
    write_header()
    nextPageToken=None
    while True:
        response = request_playlist(nextPageToken)

        with open(filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
        
            for item in response['items']:
                publishedAt, title, description, id_ = get_attributes(item)
                
                csv_writer.writerow([publishedAt, title, description, id_])
        
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

def write_header():
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['publishedAt', 'title', 'description', 'id'])

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

playlist()