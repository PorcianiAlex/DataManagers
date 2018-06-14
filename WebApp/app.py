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


@app.route('/')
def main():
    trends = get_trends()
    return render_template('index_second.html', trends= trends)

@app.route('/request', methods=['GET', 'POST'])
def request():
    if req.method == 'GET':
      result = req.args
   #   render_template()
      print(result['url'])
      if result["url"] in ['https://twitter.com/nytimes/status/1007185900894412800',
                           'https://twitter.com/nytimes/status/1007212337672179712',
                           'https://twitter.com/_BenStam/status/1006949386604171273',
                           'https://twitter.com/alienufovideos/status/1006612031280173057'
                           ]:
          return check_already_read(result['url'])
      res = json.loads(evaluator.evaluate([result["url"]]))
      score = dict()
      score['article_url'] = res[0]['article_url']
      if res[0]['text_evaluation'] < 0.33:
          score['text_evaluation'] = 'lightbox-green'
      elif res[0]['text_evaluation'] < 0.66:
          score['text_evaluation'] = 'lightbox-yellow'
      else:
          score['text_evaluation'] = 'lightbox-red'
      if res[0]['source_reliability'] < 0.33:
          score['source_reliability'] = 'lightbox-green'
      elif res[0]['source_reliability'] < 0.66:
          score['source_reliability'] = 'lightbox-yellow'
      else:
          score['source_reliability'] = 'lightbox-red'
      if res[0]['page_quality'] >= 1.5:
          score['page_quality'] = 'lightbox-red'
      elif res[0]['page_quality'] < 1.5 and res[0]['page_quality']>-1:
          score['page_quality'] = 'lightbox-yellow'
      else:
          score['page_quality'] = 'lightbox-green'
      score['final_score'] = int(res[0]['final_score']*100)

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



def check_already_read(url):
    if url == 'https://twitter.com/nytimes/status/1007185900894412800':
        score = {"article_url": 'https://t.co/4jR89vmwf6', # string
                 "page_quality": "lightbox-yellow", #string
                 "text_evaluation": "lightbox-green", # string
                 "source_reliability": "lightbox-green", #string
                 "final_score": 28   #integer in range [0:100]
                  }
        html = get_embed_code(url)
        return render_template('evaluation_second.html', html=html, confidence=score["final_score"],
                               page_q=score["page_quality"], text_ev=score["text_evaluation"],
                               source=score["source_reliability"])
    elif url == 'https://twitter.com/nytimes/status/1007212337672179712':
        score = {"article_url": 'https://t.co/Dkn1ecR7SM', # string
                 "page_quality": "lightbox-red", #string
                 "text_evaluation": "lightbox-green", # string
                 "source_reliability": "lightbox-green", #string
                 "final_score": 24   #integer in range [0:100]
                }
        html = get_embed_code(url)
        return render_template('evaluation_second.html', html=html, confidence=score["final_score"],
                               page_q=score["page_quality"], text_ev=score["text_evaluation"],
                               source=score["source_reliability"])
    elif url == 'https://twitter.com/_BenStam/status/1006949386604171273':
        score = {"article_url": 'https://t.co/nMFrB2Cuz6', # string
                 "page_quality": "lightbox-yellow", #string
                 "text_evaluation": "lightbox-red", # string
                 "source_reliability": "lightbox-red", #string
                 "final_score": 73   #integer in range [0:100]
                 }
        html = get_embed_code(url)
        return render_template('evaluation_second.html', html=html, confidence=score["final_score"],
                               page_q=score["page_quality"], text_ev=score["text_evaluation"],
                               source=score["source_reliability"])
    elif url == 'https://twitter.com/alienufovideos/status/1006612031280173057':
        score = {"article_url": 'https://t.co/goZaVi6aV2', # string
                 "page_quality": "lightbox-yellow", #string
                 "text_evaluation": "lightbox-red", # string
                 "source_reliability": "lightbox-red", #string
                 "final_score": 86   #integer in range [0:100]
                 }
        html = get_embed_code(url)
        return render_template('evaluation_second.html', html=html, confidence=score["final_score"],
                               page_q=score["page_quality"], text_ev=score["text_evaluation"],
                               source=score["source_reliability"])
    elif url == 'https://twitter.com/chewybooey1/status/1007253960527417344':
        score = {"article_url": 'http://www.thisboss.net/2018/06/13/cia-agent-gives-sworn-statement-we-brought-down-the-twin-towers-on-9-11/',  # string
                 "page_quality": "lightbox-yellow",  # string
                 "text_evaluation": "lightbox-red",  # string
                 "source_reliability": "lightbox-red",  # string
                 "final_score": 97  # integer in range [0:100]
                 }
