import csv
import requests
import time
from operator import itemgetter
from tqdm import tqdm

start = time.time()

filename = 'data/test.csv'

url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
response = requests.get(url)
article_ids = response.json()

def articles():
    write_header()
    for article_id in tqdm(article_ids):
        url = f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json"
        response = requests.get(url)
        response_dict = response.json()
        time, title, type_, url, hn_url, by, comments = get_attributes(response_dict, article_id)
        
        with open(filename, 'a', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([article_id, time, title, type_, url, hn_url, by, comments])


def write_header():
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id', 'time', 'title', 'type', 'url', 'hn_url', 'by', 'comments'])

def get_attributes(d, article_id):
    time, title, type_, url, hn_url, by, comments = None, None, None, None, None, None, None
    try:
        time = d['time']
        title = d['title']
        type_ = d['type']
        url = d['url']
        hn_url = f"http://news.ycombinator.com/item?id={article_id}"
        by = d['by']
        comments = d['descendants']
    except (KeyError) as e:
        print(f'KeyError:{article_id} {e}')

    return time, title, type_, url, hn_url, by, comments

articles()

finish = time.time()
mins = round((finish - start)/60, 2)
print(f"\nTotal time taken {mins} minutes.")