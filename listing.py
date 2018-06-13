import json
import tldextract as tld


def get_fake_site_info(url):
    """
    :param url: string
    :return: string obtained by joining a dict with keys: 'type', '2nd type', '3rd type', 'Source Notes (things to know?)'.
             The latter keys don't have a value in most cases.
    """
    ext = tld.extract(url)
    clean_url = '.'.join(ext[1:])
    with open('blacklist.json') as jsonfile:
        fake_news_urls = json.load(jsonfile)
        if clean_url in fake_news_urls:
            return 0
        else:
            return 1
#        try:
#            return 'site characteristics: ' + ', '.join([value for value in fake_news_urls[clean_url].values() if value != ''])
#        except:
#            return 'site characteristics: this site is not known for spreading fake news.'

                # stub of dict in case it is needed
                #{'type': 'this site is not known for spreading fake news.',
                #    '2nd type': '',
                #    '3rd type': '',
                #    'Source Notes (things to know?)': ''
                #    }


def add_site_to_list(url, *args):
    """
    :param url: url to add
    :param args: tuple containing 4 strings.
    :return:
    """
    ext = tld.extract(url)
    clean_url = '.'.join(ext[1:])
    with open('blacklist.json', 'r+') as jsonfile:
        fake_news_urls = json.load(jsonfile)
        fake_news_urls[clean_url] = {'type': args[0],
                                     '2nd type': args[1],
                                     '3rd type': args[2],
                                     'Source Notes (things to know?)': args[3]
                                     }
        jsonfile.seek(0)
        jsonfile.truncate()
        json.dump(fake_news_urls, jsonfile)
