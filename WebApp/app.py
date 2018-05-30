from flask import Flask, render_template, request as req
from WebApp.twitter_api import get_trends, get_embed_code
from kay import Kay

app = Flask(__name__)
evaluator = Kay()


@app.route('/')
def main():
    trends = get_trends()
    return render_template('index_second.html', trends= trends)

@app.route('/request', methods=['GET', 'POST'])
def request():
    if req.method == 'POST':
      result = req.form
      score = evaluator.evaluate(result["url"])
      html = get_embed_code(result["url"])
    return render_template('evaluation_second.html', html=html, score=score)

#if __name__ == '__main__':
#    app.run(debug=True)
