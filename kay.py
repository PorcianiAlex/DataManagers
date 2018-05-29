import banner_counter as bc
import listing
import requests


def unshorten_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


class Kay(object):

    def __init__(self):
        self.banner_counter = bc.AdCounter("easylist.txt")
        # TODO: initialize ml model

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
            score.append((element, url, count, bl_info))

        return score


