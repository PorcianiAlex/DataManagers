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



def unshorten_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True) # TODO: SSLError handling
    return resp.url


class Kay(object):

    def __init__(self, name):
        self.banner_counter = bc.AdCounter("easylist.txt")
        self.clf = joblib.load('estimator_val.pkl')
        print(name)

    def evaluate(self, data_list):
        tweets = []
        articles = []
        for _, data in enumerate(data_list):
            if isinstance(data, str):
                articles.append(data)
            else:
                tweets.append(data)
        for element in tweets:
            # TODO: user/tweet analysis
            articles_urls = []
            for _ in range(len(element._json['entities']['urls'])):
                articles_urls.append(element._json['entities']['urls'][_]['expanded_url'])
            articles.extend(articles_urls)

        score = []
        for element in articles:
            start = gstart = time.time()
            url = unshorten_url(element)
            print("unshortening: {}".format(time.time()-start))
            start = time.time()
            count = self.banner_counter.iframe_detector(url) + self.banner_counter.count_ads(url)
            print("banner counter: {}".format(time.time() - start))
            start = time.time()
            bl_info = listing.get_fake_site_info(url)
            print("blacklisting: {}".format(time.time() - start))
            start = time.time()
            txt = scrape(url)
            print("scraping: {}".format(time.time() - start))
            start = time.time()
            features = ml.extract_features(txt)
            print(features)
            features.append(count)
            print(features)
            features = np.asarray(features).reshape(1, -1)
            print("svm: {}".format(time.time() - start))
            start = time.time()
            print(features)
            res = self.clf.predict_proba(features)
            print("prediction: {}".format(time.time() - start))
            print(res[0][0])
            user_type = "stronzo"
            score.append({"received_url": element, # string
                          "unshortened_url": url, # string
                          "blacklist": bl_info, #string
                          "evaluation": res[0][0], # float
                          "user_evaluation": user_type #string
                          })
            print("total time: {}".format(time.time() - gstart))
        return json.dumps(score)
