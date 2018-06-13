import pickle as pk
import pandas as pd
import tweepy
import indicoio
import numpy as np
import features_extractor as ml
from banner_counter import AdCounter
from sklearn.externals import joblib
import listing


test_csv = pd.read_csv('test.csv', sep='\t')

APP_KEY, APP_SECRET = "52uvSUMNZaUayWR43pzAwFcMy", "nGjYIbIshdOQDb1zNWRCVIzUtvZHeih8zOmiS21eoFQeqt1Tmk"
ACC_TOKEN, ACC_TOKEN_SECRET = "989427693031739393-3bBGn4gT6k1c2T59AMDlylfvX1346S2", "RAP5YEXnVGfTEkgCsREd6ipA0QojD44ONKsTFBT1RShck"
auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(ACC_TOKEN, ACC_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

personality_clf = joblib.load('estimator_pers_full_4_feat.pkl')
indicoio.config.api_key = '42fd1c521599079dab79ef889bc9c676'
clf = joblib.load('estimator_val.pkl')
banner_counter = AdCounter("easylist.txt")
'''
#evaluator = Kay(__name__, api)
users = set()
for row in test_csv.iterrows():
    users.add(row[1][1])

pers_dict = dict()

for el in users:
    print(el)
    statuses = api.user_timeline(el, count=50)
    website = []
    urls = []
    for st in statuses[:5]:
        try:
            for i in range(len(st._json['entities']['urls'])):
                website.append(st._json['entities']['urls'][i]['expanded_url'])
                count = banner_counter.count_ads_th(st._json['entities']['urls'][i]['expanded_url']) + banner_counter.iframe_detector(st._json['entities']['urls'][i]['expanded_url'])
                urls.append((count - 15.12200866779725) / 11.892945461889907)
        except:
            pass
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
    url = np.mean(urls)
    bl_info = listing.get_fake_site_info(website[0])
    if bl_info == 0:
        page_quality = False
    else:
        page_quality = url
    pers_dict[el] = {'pers': personality_clf.predict_proba([[op, ag, ex, co]])[0][0],
                     'banner': page_quality}

with open('pers_dict.pkl', 'wb') as f:
    pk.dump(pers_dict, f)
'''

with open('pers_dict.pkl', 'rb') as f:
    pers_dict = pk.load(f)

print(pers_dict)

new_feat = []

for row in test_csv.iterrows():
    try:
        features = ml.extract_features(row[1][3])
        features.append(pers_dict[row[1][1]]['banner'])
        features = np.asarray(features).reshape(1, -1)
        text_value = clf.predict_proba(features)
        pers_value = pers_dict[row[1][1]]['pers']
        pq = pers_dict[row[1][1]]['banner']
        new_feat.append((pers_value, text_value, pq, row[1][-1]))
        if row[0] % 100 == 0:
            print(row[0])
            print((pers_value, text_value, pq, row[1][-1]))
    except Exception as e:
        print(e)

df = pd.DataFrame(new_feat, columns=['personality', 'text', 'pq', 'label'])
df.to_csv('regr.csv', sep=',')
print('done')