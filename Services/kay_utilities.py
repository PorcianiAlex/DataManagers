
# @author 'Luca Vavassori'

import requests as req
import re

'''
This script consists of utilities useful in the main script of KAY
'''

def findurls(string):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    result = []
    for url in urls:
        result.extend(url.split())
    return result

def is_twitter(url):
    r = req.get(url)
    print(re.findall('http[s]?://twitter.com/)+', r.url))

urlretrive("https://t.co/rm8w43kHBU")
