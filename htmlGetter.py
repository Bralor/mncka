import csv
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import os
import unicodedata
from urllib.parse import urlparse, urljoin


def is_absolute(url):
    return bool(urlparse(url).netloc)


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except:  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def strip_faking_text(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text


def give_me_data(url):
    req = requests.get(url)
    req.encoding = 'utf-8'
    return req.text


def find_menicko_link(url):
    req = requests.get(url)
    req.encoding = 'utf-8'

    soup = BeautifulSoup(req.text, 'html.parser')
    all_links = {a.get('href'): strip_faking_text(a.text)
                 for a in soup.find_all('a', href=True)}

    keywords = ['poledni-menu', 'denni-menu', 'tydenni-menu',
                'obedove-menu', 'tydenni', 'obedove' 'poledni', 'denni', 'menicko']
    for link, val in all_links.items():
        # print(link, val)
        # os.system("pause")
        for key in keywords:
            if key in link or key in val:
                if is_absolute(link):
                    return link
                else:
                    return urljoin(url, link)
    return url

# def load_data_as_txt(filename):
#     return [line.rstrip('\n') for line in open(filename)]


def load_data(filename):
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)  # , delimiter=';'
        return list(reader)

if __name__ == "__main__":
    load = load_data('urls.csv')
    # os.system("pause")
    for link in load:
        menu_link = find_menicko_link(link[0])
        print(menu_link)
        # html = give_me_data(menu_link)                    # pro petulku
