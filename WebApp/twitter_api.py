import tweepy

def twitter_authentication():
    # Twitter Authentication

    APP_KEY, APP_SECRET = "52uvSUMNZaUayWR43pzAwFcMy", "nGjYIbIshdOQDb1zNWRCVIzUtvZHeih8zOmiS21eoFQeqt1Tmk"
    ACC_TOKEN, ACC_TOKEN_SECRET = "989427693031739393-3bBGn4gT6k1c2T59AMDlylfvX1346S2", "RAP5YEXnVGfTEkgCsREd6ipA0QojD44ONKsTFBT1RShck"
    auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True)

def get_trends():

    api = twitter_authentication()
    json = api.trends_place(23424977)
    jsontrends = json[0]['trends']
    trends = []
    for trend in jsontrends:
        trends.append(trend['name'])

    return trends[:15]

def get_embed_code(url_form):

    api = twitter_authentication()
    json = api.get_oembed(url=url_form)
    return json["html"]
