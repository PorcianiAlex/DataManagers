import json
import tldextract as tld


def get_fake_site_info(url):
    """
    :param url: string
    :return: dict with keys: 'type', '2nd type', '3rd type', 'Source Notes (things to know?)'.
             The first key is always present, the others only in rare cases
    """
    ext = tld.extract(url)
    clean_url = '.'.join(ext[1:])
    with open('blacklist.json') as jsonfile:
        fake_news_urls = json.load(jsonfile)
        try:
            return fake_news_urls[clean_url]
        except:
            return {'type': 'this site is not known for spreading fake news.'}
