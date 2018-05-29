if __name__ == '__main__':
    import twitter_bot as tb
    import tweepy
    import multiprocessing as mp
    import threading as th

    myStreamListener = tb.MyStreamListener()
    myStream = tweepy.Stream(auth=myStreamListener.api.auth, listener=myStreamListener)
    print('system on')
    userStream = mp.Process(target=myStream.userstream)
    userStream.start()