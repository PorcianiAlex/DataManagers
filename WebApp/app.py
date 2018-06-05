from flask import Flask, render_template, request as req
from WebApp.twitter_api import get_trends, get_embed_code
from kay import Kay

app = Flask(__name__)
evaluator = Kay(__name__)


@app.route('/')
def main():
    #trends = get_trends()
    trends = []
    return render_template('index_second.html', trends= trends)

@app.route('/request', methods=['GET', 'POST'])
def request():
    if req.method == 'POST':
      result = req.form
      score = evaluator.evaluate(result["url"])
      html = get_embed_code(result["url"])
    return render_template('evaluation_second.html', html=html, score=score)

<<<<<<< HEAD
@app.route('/firm-db/login', methods=['GET', 'POST'])
def login():
    return render_template('firm-db/login.html')

@app.route('/firm-db/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('firm-db/dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
=======
#if __name__ == '__main__':
#    app.run(debug=True)
>>>>>>> f05058054598fb1314ee27bd0b3b087931671935
