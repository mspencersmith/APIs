"""
Reuturns attributes of playlists 
"""
import os.path
import json
from googleapiclient.discovery import build
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

path = os.path.join(BASE_DIR, 'config.json')

with open(path) as api_file:
    config = json.load(api_file)

youtube = build('youtube', 'v3', developerKey=config['API_KEY'])

nextPageToken = None

while True:
    request = youtube.playlists().list(
        part = 'contentDetails, snippet',
        channelId = 'UChh-akEbUM8_6ghGVnJd6cQ',
        maxResults = 50,
        pageToken = nextPageToken
        )
    response = request.execute()
    # items = response['items']
    # print(response)

    for item in response['items']:
        id_ = item['id']
        snippet = item['snippet']
        publishedAt = snippet['publishedAt']
        title = snippet['title']
        description = snippet['description']
        print(f'{publishedAt},{title},{description},{id_}')
        # print(item)
        print()

    nextPageToken = response.get('nextPageToken')

    if not nextPageToken:
        break