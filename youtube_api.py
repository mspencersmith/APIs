import os.path
import json
from googleapiclient.discovery import build
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

path = os.path.join(BASE_DIR, 'config.json')

with open(path) as api_file:
    config = json.load(api_file)

youtube = build('youtube', 'v3', developerKey=config['API_KEY'])

request = youtube.channels().list(
    part='statistics',
    forUsername='bwf'
    )
response = request.execute()

print(response)