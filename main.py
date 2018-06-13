import twitter_bot as tb
import tweepy
import multiprocessing as mp
import WebApp.app as wa

def main():



    APP_KEY, APP_SECRET = "52uvSUMNZaUayWR43pzAwFcMy", "nGjYIbIshdOQDb1zNWRCVIzUtvZHeih8zOmiS21eoFQeqt1Tmk"
    ACC_TOKEN, ACC_TOKEN_SECRET = "989427693031739393-3bBGn4gT6k1c2T59AMDlylfvX1346S2", "RAP5YEXnVGfTEkgCsREd6ipA0QojD44ONKsTFBT1RShck"
    auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_TOKEN_SECRET)
    api = tweepy.API(auth)
    myStreamListener = tb.MyStreamListener(api)
    myStream = tweepy.Stream(auth=myStreamListener.api.auth, listener=myStreamListener)
    userStream = mp.Process(target=myStream.userstream)
    userStream.start()
    print('chatbot on')
    #wa.app.run(debug=True, use_reloader=False)
    app = wa.app
    app.run(debug=True, use_reloader=False)
    print('web app on')


if __name__ == '__main__':
    main()
