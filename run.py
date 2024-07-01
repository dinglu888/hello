import os

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return '欢迎使用微信云托管========！'

@app.route('/add', methods=['POST', 'GET'])
def add(a, b):
    return a+b;

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
