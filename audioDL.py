import requests
import urllib.request
import re
from bs4 import BeautifulSoup

url = input("Enter the URL of the website you would like to scrape from.")

r = requests.get(str(url))
soup = BeautifulSoup(r.content, 'html.parser')

for a in soup.find_all('a', href=re.compile('http.*\.mp3')):
    doc = requests.get(a['href'])
    filename = a['href'][a['href'].rfind("/")+1:]
    with open(filename, 'wb') as f:
        f.write(doc.content)
