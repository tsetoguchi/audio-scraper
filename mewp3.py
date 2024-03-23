# -*- coding: utf-8 -*-
from selectolax.parser import HTMLParser
from typing import List, Optional
from urllib.parse import urljoin
import requests
import re

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                   'Safari/537.36'}

def find_mp3_links(url: str) -> Optional[List[str]]:
    response = requests.get(url, headers=header, timeout=5)
    if response.status_code == 200:
        html = response.text
        mp3_links = re.findall(r'"file":"(.*?\.mp3)"', html)
        return mp3_links
    else:
        print("Failed to fetch the webpage:", response.status_code)
        return None

def download_mp3(url: str, output_path: str) -> None:
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {output_path}")
    else:
        print(f"Failed to download: {url}")

if __name__ == "__main__":
    url = "https://archive.org/details/antichrist_librivox_?webamp=default"
    #url = input("Link to site you want to check for .mp3s: ")
    base_url = '/'.join(url.split('/')[:-1])  # Get base URL of the webpage
    mp3_links = find_mp3_links(url)
    if mp3_links:
        print("MP3 Links found:")
        for idx, link in enumerate(mp3_links, start=1):
            print(f"{idx}. {link}")
            absolute_url = urljoin(base_url, link)
            download_path = f"mp3_{idx}.mp3"
            download_mp3(absolute_url, download_path)
    else:
        print("No MP3 links found on the webpage.")
