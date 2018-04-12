from app.providers.Steganography import *
from flask import request
import time
import os

STATIC = 'static/images/'
LINK = '../{}'.format(STATIC)
ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT, LINK)


def steganography():
    if not os.path.isdir(PATH):
        os.mkdir(PATH)
    if 'cover' not in request.files:
        return False
    if 'secret' not in request.files:
        return False

    cover = request.files['cover']
    secret = request.files['secret']
    cover_name = cover.filename
    secret_name = secret.filename
    base_name = str(int(round(time.time() * 1000))) + '_{}'
    encode_name = base_name.format("encode.png")
    decode_name = base_name.format("decode.png")

    cover.save(os.path.join(PATH, cover_name))
    secret.save(os.path.join(PATH, secret_name))

    bit = int(request.form['bit'])
    plane = int(request.form['plane'])
    cover_src = PATH + '{}'.format(cover_name)
    secret_src = PATH + '{}'.format(secret_name)
    encode_src = PATH + '{}'.format(encode_name)
    decode_src = PATH + '{}'.format(decode_name)

    msb = MSB()
    msb.encode(cover_src, secret_src, plane, bit).save(encode_src)
    msb.decode(encode_src, plane, bit).save(decode_src)

    result = dict(
        cover=STATIC + '{}'.format(cover_name),
        secret=STATIC + '{}'.format(secret_name),
        encode=STATIC + '{}'.format(encode_name),
        decode=STATIC + '{}'.format(decode_name)
    )
    return result
