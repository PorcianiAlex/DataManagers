import banner_counter as bc
import listing
import requests
import json
from sklearn.externals import joblib
from sklearn.svm import SVC
from Scraper import scrape
import features_extractor as ml
import numpy as np
import time
import tweepy
import indicoio



def unshorten_url(url):
    resp = None
    print(url)
    try:
        session = requests.Session()  # so connections are recycled
        resp = session.head(url, allow_redirects=True) # TODO: SSLError handling
    except Exception as e:
        print(e)
        session = requests.Session()  # so connections are recycled
        resp = session.head(url, allow_redirects=True)  # TODO: SSLError handling
    return resp.url


class Kay(object):

    def __init__(self, name, api):
        self.banner_counter = bc.AdCounter("easylist.txt")
        self.clf = joblib.load('estimator_val.pkl')
        self.api = api
        self.personality_clf = joblib.load('estimator_pers_full_4_feat.pkl')
        indicoio.config.api_key = '42fd1c521599079dab79ef889bc9c676'
        self.log_reg = joblib.load('log_reg.pkl')
        print(name)

    def evaluate(self, data_list):
        gstart = time.time()
        tweets = []
        articles = []
        tweets_text = []
        tweets_username = []
        for _, data in enumerate(data_list):
            if isinstance(data, str):
                articles.append(data)
            else:
                tweets.append(data)
        for element in tweets:
            articles_urls = []
            for _ in range(len(element._json['entities']['urls'])):
                articles_urls.append(element._json['entities']['urls'][_]['expanded_url'])
                print(articles_urls)
            tweets_text.append(element._json['full_text'])
            tweets_username.append(element._json['user']['id'])
            articles.extend(articles_urls)

        score = []
        user_eval = []
        article_eval = []
        page_quality = []
        urls = []
        final = []
        start = time.time()
        for us in tweets_username:
            statuses = self.api.user_timeline(us, count=50)
            pers_values = []
            for elem in statuses:
                txt = elem.text
                words = txt.split(' ')
                for word in words[::-1]:
                    if '@' in word:
                       words.remove(word)
                    elif 'http' in word:
                        words.remove(word)
                if words:
                    try:
                        pers = indicoio.personality(' '.join(words))
                        pers_values.append(pers)
                    except Exception as e:
                        print(e)
            op = np.mean([pers_values[i]['openness'] for i in range(len(pers_values))])
            ag = np.mean([pers_values[i]['agreeableness'] for i in range(len(pers_values))])
            ex = np.mean([pers_values[i]['extraversion'] for i in range(len(pers_values))])
            co = np.mean([pers_values[i]['conscientiousness'] for i in range(len(pers_values))])

            user_eval.append(self.personality_clf.predict_proba([[ag, co, ex, op]])[0][0])
        print('personality: {]'.format(time.time() - start))


        for element in articles:
            start = time.time()
            url = unshorten_url(element)
            urls.append(url)
            print("unshortening: {}".format(time.time()-start))
            start = time.time()
            count = self.banner_counter.iframe_detector(url) + self.banner_counter.count_ads_th(url)
            print("banner counter: {}".format(time.time() - start))
            start = time.time()
            bl_info = listing.get_fake_site_info(url)
            if bl_info == 0:
                page_quality.append(False)
            else:
                page_quality.append((count-15.12200866779725)/11.892945461889907)
            print("blacklisting: {}".format(time.time() - start))
            start = time.time()
            txt = scrape(url)
            print("scraping: {}".format(time.time() - start))
            start = time.time()
            features = ml.extract_features(txt)
            features.append(count)
            features = np.asarray(features).reshape(1, -1)
            print("svm: {}".format(time.time() - start))
            start = time.time()
            res = self.clf.predict_proba(features)
            print("prediction: {}".format(time.time() - start))
            article_eval.append(res[0][0])
            final.append(self.log_reg.predcit_proba([user_eval[0], article_eval[0], page_quality[0]]))
            print("total time: {}".format(time.time() - gstart))

            print('article eval vs final score: {} vs {}'.format(article_eval[0], final[0]))

        score.append({# "tweet_url": element,  # string
                      "article_url": urls[0],  # string
                      "page_quality": page_quality[0],  # string
                      "text_evaluation": article_eval[0],  # string
                      "source_reliability": user_eval[0],  # string
                      "final_score": article_eval[0]
                      })
        return json.dumps(score)
