from flask import Flask, render_template, request as req
#from WebApp.twitter_api import get_trends, get_embed_code
from twitter_api import get_trends, get_embed_code
import json
import builtins
#from kay import Kay

app = Flask(__name__)
#evaluator = Kay()


@app.route('/')
def main():
    trends = get_trends()
    return render_template('index_second.html', trends= trends)

@app.route('/request', methods=['GET', 'POST'])
def request():
    if req.method == 'GET':
      result = req.args
      #score = evaluator.evaluate(result["url"])
      score = {"tweet_url": 0, # string
                "article_url": 0, # string
                "page_quality": "lightbox-red", #string
                "text_evaluation": "lightbox-red", # string
                "source_reliability": "lightbox-yellow", #string
                "final_score": 83   #integer in range [0:100]
               }
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

if __name__ == '__main__':
    app.run(debug=True)
