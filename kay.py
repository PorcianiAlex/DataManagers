import banner_counter as bc
import listing
import requests
import json
from sklearn.externals import joblib
from sklearn.svm import SVC
from Scraper import scrape
import features_extractor as ml



def unshorten_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


class Kay(object):

    def __init__(self, name):
        self.banner_counter = bc.AdCounter("easylist.txt")
        self.clf = joblib.load('estimator.pkl')
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
            url = unshorten_url(element)
            count = self.banner_counter.iframe_detector(url) + self.banner_counter.count_ads(url)
            bl_info = listing.get_fake_site_info(url)
            txt = scrape(url)
            features = ml.extract_features(txt).reshape(1,-1) # .append(count)
            eval = self.clf.predict_proba(features) # TODO: scaling first
            print(eval[0][0])
            user_type = "stronzo"
            score.append({"received_url": element, # string
                          "unshortened_url": url, # string
                          "blacklist": bl_info, #string
                          "evaluation": eval[0][0], # float
                          "user_evaluation": user_type #string
                          })

        return json.dumps(score)
