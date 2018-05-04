# import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

###beforeitnews.com

req = Request('http://beforeitsnews.com/opinion-conservative/2018/05/kim-jong-un-is-another-hitler-do-not-be-deceived-video-3377422.html')
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

text = " ".join(entries) #salvare text

print(text)