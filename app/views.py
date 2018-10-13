import os
import time
import cv2
from flask import request
from app.providers.stegano import LSB
from app.providers.Steganography import *

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


def steganoencode():
    if not os.path.isdir(PATH):
        os.mkdir(PATH)
    if 'cover' not in request.files:
        return False

    cover = request.files['cover']
    cover_image = os.path.join(PATH, '%s.jpg' % str(int(round(time.time() * 1000))))
    cover.save(cover_image)

    steg = LSB(img_path=cover_image, _src='')
    if 'message' in request.form:
        _encode_img = steg.encode_msg(msg=request.form['message'])
    elif 'secret' in request.files:
        _secret = request.files['secret']
        _secret_image = os.path.join(PATH, '%s.jpg' % str(int(round(time.time() * 1000))))
        _secret.save(cover_image)
        _encode_img = steg.encode_image(img_path=_secret_image)

    cv2.imwrite("static/images/stegano_test.png", _encode_img)
    return ['encode']


def steganodecode():
    return ['decode']
