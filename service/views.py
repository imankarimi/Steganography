import os
import time
import cv2
from flask import request
from service.Providers.stegano import LSB
from service.Providers.Steganography import MSB

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

    _unique_name = int(round(time.time() * 1000))
    cover = request.files['cover']
    cover_image = os.path.join(PATH, 'cover_%s.jpg' % str(_unique_name))
    cover.save(cover_image)

    steg = LSB(img_path=cover_image)
    try:
        if 'message' in request.form and request.form['message']:
            _encode_img = steg.encode_msg(msg=request.form['message'])
        elif 'secret' in request.files:
            _secret = request.files['secret']
            _secret_image = os.path.join(PATH, 'secret_%s.jpg' % str(_unique_name))
            _secret.save(_secret_image)
            _encode_img = steg.encode_image(img_path=_secret_image)
        else:
            return {'valid': False, 'type': 'encode', 'message': 'field required'}
    except Exception as e:
        return {'valid': False, 'type': 'encode', 'message': str(e)}

    image = 'static/images/encode_%s.png' % str(_unique_name)
    cv2.imwrite(image, _encode_img)
    result = {'valid': True, 'type': 'encode', 'encode_image': image, 'name': 'encode_%s.png' % str(_unique_name)}
    return result


def steganodecode():
    _unique_name = int(round(time.time() * 1000))
    cover = request.files['cover']
    cover_image = os.path.join(PATH, 'encode_%s.png' % str(_unique_name))
    cover.save(cover_image)
    steg = LSB(img_path=cover_image)
    if request.form['decode'] == '0':
        decode_msg = steg.decode_msg()
        return {'valid': True, 'type': 'decode', 'message': decode_msg}
    else:
        decode_img = steg.decode_image()
        image = 'static/images/decode_%s.png' % str(_unique_name)
        cv2.imwrite(image, decode_img)
        return {'valid': True, 'type': 'decode', 'decode_img': image, 'name': 'decode_%s.png' % str(_unique_name)}
