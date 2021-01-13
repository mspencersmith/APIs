import csv
import requests
import time
from datetime import date
from tqdm import tqdm

start = time.time()
today = date.today()
filename = f'data/{today}.csv'

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
response = requests.get(url, headers=headers)
response_dict = response.json()
repo_dicts = response_dict['items']

with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['id', 'name', 'private', 'owner', 'url', 'description', 'stars'])

for repo_dict in tqdm(repo_dicts):
    id_ = repo_dict['id']
    name = repo_dict['name']
    private = repo_dict['private']
    owner = repo_dict['owner']['login']
    url = repo_dict['html_url']
    description = repo_dict['description']
    stars = repo_dict['stargazers_count']

    with open(filename, 'a', newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([id_, name, private, owner, url, description, stars])

finish = time.time()
secs = round((finish - start), 2)
print(f"\nTotal time taken {secs}s.")