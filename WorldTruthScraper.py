# import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pickle as pk

# Scraper for WorldTruthTv.com

url = 'https://worldtruth.tv/do-you-have-rh-negative-blood-new-theory-suggests-your-dna-doesnt-come-from-earth/'
req = Request(url, headers= {'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

body = soup.find(attrs={"id": "body"})

b = body.find_all("p")

entries = []
for p in b:
    a = p.find_all("a")

    if not p.style and p.text.strip() and len(a)==0: #scarto il paragrafo se c'è un link con len(a)==0
        entries.append(p.text)

# create the complete text
text = " ".join(entries)

print(text)