import cv2 as cv
from app.providers.stegano import LSB

# encode_lsb = LSB(image_path='static/images/cover.jpg')
# img_encoded = encode_lsb.encode_message(message="سلام استاد تست این عکس اوکی بود بهم پیام بدین لطفا. با تشکر")
# cv.imwrite("static/images/stegano_test.png", img_encoded)
#
#
# decode_lsb = LSB(image_path='static/images/stegano_test.png')
# decode_message = decode_lsb.decode_message()
# print(decode_message)

#encoding
# steg = LSB(image_path='static/images/cover.jpg')
# new_im = steg.encode_image(image_path='static/images/secret.jpg')
# cv.imwrite("static/images/new_image.png", new_im)

#decoding
# steg = LSB(_src='', img_path="static/images/new_image.png")
# orig_im = steg.decode_image()
# cv.imwrite('static/images/iman.png', orig_im)
