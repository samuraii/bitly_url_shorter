from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
import os
import argparse

load_dotenv()
token = os.getenv("TOKEN")


def get_bitlink(token, url):
    shorten_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization': 'Bearer ' + token}
    data = {"long_url": url}
    response = requests.post(url=shorten_url, headers=headers, json=data)
    if not response.ok:
        raise Exception(response.json()['description'])
    return response.json()['link']


def get_link_clicks(token, bitlink):
    clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/referring_domains'
    headers = {'Authorization': 'Bearer ' + token}
    data = {"unit": "month"}
    response = requests.get(url=clicks_url, headers=headers, json=data)
    if not response.ok:
        raise Exception(response.text)
    return response.json()['metrics'][0]['clicks']


def is_biltink(token, bitlink):
    check_link_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url=check_link_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('url', help='url to short')
    args = parser.parse_args()
    url = args.url

    if is_biltink(token, url):
        clicks = get_link_clicks(token, url)
        print(f"Bitlink: {url} was clicked {clicks} times")
    else:
        print(f"Bitlink for {url} is {get_bitlink(token, url)}")
