from flask import Flask, render_template, request as req
from twitter_api import get_trends, get_embed_code

app = Flask(__name__)

@app.route('/')
def main():
    trends = get_trends()
    return render_template('index_second.html', trends= trends)

@app.route('/request', methods=['GET', 'POST'])
def request():
    if req.method == 'POST':
      result = req.form
      html = get_embed_code(result["url"])
    return render_template('evaluation_second.html', html=html)

if __name__ == '__main__':
    app.run(debug=True)
