from flask import Flask, render_template, request as req
from WebApp.twitter_api import get_trends, get_embed_code
#from twitter_api import get_trends, get_embed_code
import json
import tweepy
from kay import Kay

Consumer_Key ='HGHfSdL36UbXtRzreZWh0oQ3T'
Consumer_Secret ='RE5GvxSMzsRpggUKZaFYvccXb8XnnIc5muxnkvXGCwpi75WMUn'

Access_Token ='552114566-bER0sfck1sWKt7qybzbY8P5oOhiVANoetrOCKIb2'
Access_Token_Secret='Zx0ux4xh0xYYwsSmtt67DuD79DXrxq88zBKffSJ3OXXGy'

auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)


app = Flask(__name__)
evaluator = Kay(__name__, api)
'''
class subFlask(Flask):
    def __init__(self):
        self.evaluator = None
        super().__init__(__name__)

    def set_kay(self, api):
        self.evaluator = Kay(__name__, api)


app = subFlask()
'''

@app.route('/')
def main():
    trends = get_trends()
    return render_template('index_second.html', trends= trends)

@app.route('/request', methods=['GET', 'POST'])
def request():
    if req.method == 'GET':
      result = req.args
   #   render_template()
      res = evaluator.evaluate([result["url"]])
      score = dict()
      score['article_url'] = res['article_url']
      if res['text_evaluation'] < 0.33:
          score['text_evaluation'] = 'lightbox-green'
      elif res['text_evaluation'] < 0.66:
          score['text_evaluation'] = 'lightbox-yellow'
      else:
          score['text_evaluation'] = 'lightbox-red'
      if res['source_reliability'] < 0.33:
          score['source_reliability'] = 'lightbox-green'
      elif res['source_reliability'] < 0.66:
          score['source_reliability'] = 'lightbox-yellow'
      else:
          score['source_reliability'] = 'lightbox-red'
      if res['page_quality'] == False or res['page_quality'] >= 1.5:
          score['page_quality'] = 'lightbox-red'
      elif res['page_quality'] < 1.5 and res['page_quality']>-1:
          score['page_quality'] = 'lightbox-yellow'
      else:
          score['page_quality'] = 'lightbox-green'
      score['final_score'] = int(res['final_score']*100)

      '''
      score = {"tweet_url": 0, # string
                "article_url": 0, # string
                "page_quality": "lightbox-red", #string
                "text_evaluation": "lightbox-red", # string
                "source_reliability": "lightbox-yellow", #string
                "final_score": 83   #integer in range [0:100]
               }
        '''
    html = get_embed_code(result["url"])
    return render_template('evaluation_second.html', html=html, confidence=score["final_score"], page_q=score["page_quality"], text_ev=score["text_evaluation"], source=score["source_reliability"])

@app.route('/firm-db/login', methods=['GET', 'POST'])
def login():
    return render_template('firm-db/login.html')

@app.route('/firm-db/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('firm-db/dashboard.html')

@app.route('/firm-db/user', methods=['GET', 'POST'])
def user():
    return render_template('firm-db/user.html')

@app.route('/firm-db/table', methods=['GET', 'POST'])
def table():
    return render_template('firm-db/table.html')

@app.route('/firm-db/notifications', methods=['GET', 'POST'])
def notifications():
    return render_template('firm-db/notifications.html')


#if __name__ == '__main__':
#    app.run(debug=True)
