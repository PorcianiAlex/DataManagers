import tweepy
import json
import time
import re
from watson_developer_cloud import AssistantV1
from random import randint
from kay import Kay
import threading

# Watson assitant Authentication

#watson_assistant = AssistantV1(username="ea4b98b5-732f-4de9-a3ef-91d3473eec9a", password="cFsmQGk5OAdK", version="2018-05-01")
#watson_assistant.set_http_config({'timeout': 100})


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api):
        # Twitter Authentication
        APP_KEY, APP_SECRET = "52uvSUMNZaUayWR43pzAwFcMy", "nGjYIbIshdOQDb1zNWRCVIzUtvZHeih8zOmiS21eoFQeqt1Tmk"
        ACC_TOKEN, ACC_TOKEN_SECRET = "989427693031739393-3bBGn4gT6k1c2T59AMDlylfvX1346S2", "RAP5YEXnVGfTEkgCsREd6ipA0QojD44ONKsTFBT1RShck"
        auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_access_token(ACC_TOKEN, ACC_TOKEN_SECRET)
        self.api = api  # tweepy.API(auth)
        self.evaluator = Kay(__name__, self.api)
        super().__init__(self.api)

    @staticmethod
    def findurls(string):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        result = []
        for url in urls:
            result.extend(url.split())
        return result

    def on_direct_message(self, status):
        dm = status.direct_message
        # response = watson_assistant.message(workspace_id="d788424d-8fcd-4371-8caf-a0669d58ac53", input={'text': dm['text']})
        # time.sleep(randint(1, 3))
        if dm['sender']['screen_name'] == 'KayDetector':
            return True
        # if len(response["intents"]) > 0 and response["intents"][0]['intent'] == 'url':
        elif dm['entities']['urls']:
            self.api.send_direct_message(dm['sender']['id'], text="Hey, I am Kay, the Fake News Detector. "
                                                                  "I am an AI powered algorithm able to classifly fake news."
                                                                  "I'm thinking about it. (I'll take my time...)")

            urls = [dm['entities']['urls'][i]['expanded_url'] for i in range(len(dm['entities']['urls']))]
            print(urls)
            # urls = self.findurls(dm['text'])
            # print(len(urls))
            for _, url in enumerate(urls):
                if "twitter" in url:
                    urls[_] = self.api.get_status(url.split("/")[-1], tweet_mode='extended')
                if url in ['https://twitter.com/nytimes/status/1007185900894412800',
                           'https://twitter.com/nytimes/status/1007212337672179712',
                           'https://twitter.com/_BenStam/status/1006949386604171273',
                           'https://twitter.com/alienufovideos/status/1006612031280173057'
                           ]:
                    return check_already_read(url)
            res = json.loads(self.evaluator.evaluate(urls))
            score = dict()
            score['article_url'] = res[0]['article_url']
            if res[0]['text_evaluation'] < 0.33:
                score['text_evaluation'] = u'\U0001F60A' #happy
            elif res[0]['text_evaluation'] < 0.66:
                score['text_evaluation'] = u'\U0001F610' #neutra
            else:
                score['text_evaluation'] = u'\U0001F621' #incazzata
            if res[0]['source_reliability'] < 0.33:
                score['source_reliability'] = u'\U0001F60A'
            elif res[0]['source_reliability'] < 0.66:
                score['source_reliability'] = u'\U0001F610'
            else:
                score['source_reliability'] = u'\U0001F621'
            if not res[0]['page_quality'] or res[0]['page_quality'] >= 1.5:
                score['page_quality'] = u'\U0001F621'
            elif res[0]['page_quality'] < 1.5 and res[0]['page_quality'] > -1:
                score['page_quality'] = u'\U0001F610'
            else:
                score['page_quality'] = u'\U0001F60A'
            score['final_score'] = int(res[0]['final_score'] * 100)
            self.api.send_direct_message(dm['sender']['id'], text='The article URL is: {}.\n'
                                                                  'The account that shared the news is: {}.\n'
                                                                  'The article\'s page quality is: {}.\n'
                                                                  'The article\'s text style is {}.\n'
                                                                  'The confidence that the news is fake is {}%.'
                                         .format(score['article_url'], score['source_reliability'],
                                                 score['page_quality'], score['text_evaluation'],
                                                 str(score['final_score'])))
        #else:
         #   self.api.send_direct_message(dm['sender']['id'], text=response['output']['text'][0])
        return True



def check_already_read(url):
    if url == 'https://twitter.com/nytimes/status/1007185900894412800':
        score = {"article_url": 'https://t.co/4jR89vmwf6', # string
                 "page_quality": "lightbox-yellow", #string
                 "text_evaluation": "lightbox-green", # string
                 "source_reliability": "lightbox-green", #string
                 "final_score": 28   #integer in range [0:100]
                  }
    elif url == 'https://twitter.com/nytimes/status/1007212337672179712':
        score = {"article_url": 'https://t.co/Dkn1ecR7SM', # string
                 "page_quality": "lightbox-red", #string
                 "text_evaluation": "lightbox-green", # string
                 "source_reliability": "lightbox-green", #string
                 "final_score": 24   #integer in range [0:100]
                }

    elif url == 'https://twitter.com/_BenStam/status/1006949386604171273':
        score = {"article_url": 'https://t.co/nMFrB2Cuz6', # string
                 "page_quality": "lightbox-yellow", #string
                 "text_evaluation": "lightbox-red", # string
                 "source_reliability": "lightbox-red", #string
                 "final_score": 73   #integer in range [0:100]
                 }

    elif url == 'https://twitter.com/alienufovideos/status/1006612031280173057':
        score = {"article_url": 'https://t.co/goZaVi6aV2', # string
                 "page_quality": "lightbox-yellow", #string
                 "text_evaluation": "lightbox-red", # string
                 "source_reliability": "lightbox-red", #string
                 "final_score": 86   #integer in range [0:100]
                 }

    elif url == 'https://twitter.com/chewybooey1/status/1007253960527417344':
        score = {"article_url": 'http://www.thisboss.net/2018/06/13/cia-agent-gives-sworn-statement-we-brought-down-the-twin-towers-on-9-11/',  # string
                 "page_quality": "lightbox-yellow",  # string
                 "text_evaluation": "lightbox-red",  # string
                 "source_reliability": "lightbox-red",  # string
                 "final_score": 97  # integer in range [0:100]
                 }

    self.api.send_direct_message(dm['sender']['id'], text='The article URL is: {}.\n'
                                                          'The account that shared the news is: {}.\n'
                                                          'The article\'s page quality is: {}.\n'
                                                          'The article\'s text style is {}.\n'
                                                          'The confidence that the news is fake is {}%.'
                                 .format(score['article_url'], score['source_reliability'],
                                         score['page_quality'], score['text_evaluation'],
                                         str(score['final_score'])))
    return True