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
nextPageToken = None
filename = 'data/bwf_playlists.csv'

with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['publishedAt', 'title', 'description', 'id'])

while True:
    request = youtube.playlists().list(
        part = 'contentDetails, snippet',
        channelId = channel_id,
        maxResults = 50,
        pageToken = nextPageToken
        )
    response = request.execute()
    # items = response['items']
    # print(response)
    with open(filename, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in response['items']:
            id_ = item['id']
            snippet = item['snippet']
            publishedAt = snippet['publishedAt']
            title = snippet['title']
            description = snippet['description']
            
            csv_writer.writerow([publishedAt, title, description, id_])

    nextPageToken = response.get('nextPageToken')

    if not nextPageToken:
        break