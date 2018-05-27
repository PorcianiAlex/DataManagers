import tweepy
import json
import time
import re
from watson_developer_cloud import AssistantV1
from random import randint
from kay import Kay

# Watson assitant Authentication

#watson_assistant = AssistantV1(username="ea4b98b5-732f-4de9-a3ef-91d3473eec9a", password="cFsmQGk5OAdK", version="2018-05-01")
#watson_assistant.set_http_config({'timeout': 100})


class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        # Twitter Authentication
        APP_KEY, APP_SECRET = "52uvSUMNZaUayWR43pzAwFcMy", "nGjYIbIshdOQDb1zNWRCVIzUtvZHeih8zOmiS21eoFQeqt1Tmk"
        ACC_TOKEN, ACC_TOKEN_SECRET = "989427693031739393-3bBGn4gT6k1c2T59AMDlylfvX1346S2", "RAP5YEXnVGfTEkgCsREd6ipA0QojD44ONKsTFBT1RShck"
        auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_access_token(ACC_TOKEN, ACC_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.evaluator = Kay()
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
        if dm['sender']['screen_name'] == 'ProjectVLADFK':
            return True
        # if len(response["intents"]) > 0 and response["intents"][0]['intent'] == 'url':
        elif dm['entities']['urls']:
            urls = [dm['entities']['urls'][i]['expanded_url'] for i in range(len(dm['entities']['urls']))]
            # urls = self.findurls(dm['text'])
            # print(len(urls))
            for _, url in enumerate(urls):
                if "twitter" in url:
                    urls[_] = self.api.get_status(url.split("/")[-1], tweet_mode='extended')
            score = self.evaluator.evaluate(urls)
            self.api.send_direct_message(dm['sender']['id'], text=score)
        #else:
         #   self.api.send_direct_message(dm['sender']['id'], text=response['output']['text'][0])
        return True



