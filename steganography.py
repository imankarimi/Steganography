from flask import Flask, jsonify, render_template, redirect, url_for, flash
from app.views import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """ python """
    return render_template('index.html')


@app.route('/embed', methods=['POST'])
def embed():
    result = steganography()
    return render_template('index.html', response=result)


@app.route('/api/v1/embed')
def embed_service():
    result = steganography()
    return jsonify(result)


if __name__ == '__main__':
    app.secret_key = '$6j1v32x+5)$d@uv)_)ek-9cb41q3+$)t20s)%la92ra#&63_*'
    app.debug = True
    app.run()
