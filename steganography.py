from flask import Flask, jsonify, render_template
from service.views import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', welcome=True)


@app.route('/stegano/encode/', methods=['GET'])
def encode():
    return render_template('index.html', encode=True)


@app.route('/stegano/decode/', methods=['GET'])
def decode():
    return render_template('index.html', decode=True)


@app.route('/api/v1/stegano/encode/', methods=['POST'])
def stegano_encode():
    result = steganoencode()
    return jsonify(result)


@app.route('/api/v1/stegano/decode/', methods=['POST'])
def stegano_decode():
    result = steganodecode()
    return jsonify(result)


if __name__ == '__main__':
    app.secret_key = '$6j1v32x+5)$d@uv)_)ek-9cb41q3+$)t20s)%la92ra#&63_*'
    app.debug = True
    app.run()
