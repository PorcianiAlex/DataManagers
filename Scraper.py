# import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

#scraper html for --- beforeitnews.com --- by Alex

def scrape(url):

    #header needs to get the permissions to get the html
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = Request(url, headers=hdr)
    page = urlopen(req).read()

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, "html.parser")

    website = url.split('.com')[0]
    print(website)

    if website=="http://www.beforeitsnews":
        body = soup.find(attrs={"id": "body"})
    elif website=="http://www.dcclothesline":
        body= soup.find(attrs={"class": "entry-content"})
    else:
        return "website not supported"

    b = body.find_all("p")

    entries = []
    for p in b:
        a = p.find_all("a")

        if not p.style and p.text.strip() and len(a)==0: #scarto il paragrafo se c'è un link con len(a)==0
            entries.append(p.text)

    text = " ".join(entries) #salvare text

    return (text)


result = scrape('http://www.beforeitsnews.com/alternative/2018/05/gun-owner-will-give-birth-in-prison-after-trying-to-protect-daughter-from-assailant-3612886.html')
print(result)