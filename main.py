import twitter_bot as tb
import tweepy
import multiprocessing as mp
import WebApp.app as wa


def main():
    myStreamListener = tb.MyStreamListener()
    myStream = tweepy.Stream(auth=myStreamListener.api.auth, listener=myStreamListener)
    userStream = mp.Process(target=myStream.userstream)
    userStream.start()
    print('chatbot on')
    wa.app.run(debug=True, use_reloader=False)
    print('web app on')


if __name__ == '__main__':
    main()
