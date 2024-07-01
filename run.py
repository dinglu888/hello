import os

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return '欢迎使用微信云托管========！';

@app.route('/getData', methods=['GET'])
def getData():
    data = {"name":"xiaoming", "age":"18"}
    return data;

@app.route('/add', methods=['POST'])
#def add(a, b):
#    return a+b;
def add():
    a1 = request.json['a'];
    b1 = request.json['b'];
    return int(a1)+int(b1);

@app.route('/search', methods=['POST'])
def search():
    keyword = request.json['keyword']
    return jsonify(keyword);


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
