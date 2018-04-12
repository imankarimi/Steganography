import numpy as np
from PIL import Image


# Most Significant Bit
class MSB:

    @staticmethod
    def encode(cover_src, secret_src, plane, bit):
        cover = image_to_matrix(cover_src)
        secret = image_to_matrix(secret_src)
        mask = 0xff ^ (1 << bit)
        secret_bits = ((secret[..., plane] >> 7) << bit)
        height, width, _ = secret.shape
        cover_plane = (cover[:height, :width, plane] & mask) + secret_bits
        cover[:height, :width, plane] = cover_plane
        img = matrix_to_image(cover)
        print("Encode Completed!")
        return img

    @staticmethod
    def decode(img, plane, bit):
        encode = image_to_matrix(img)
        change_index = [0, 1, 2]
        change_index.remove(plane)
        encode[..., change_index] = 0
        encode = ((encode >> bit) & 0x01) << 7
        exposed_secret = matrix_to_image(encode)
        print("Decode Completed!")
        return exposed_secret


# Least Significant Bit
class LSB:

    @staticmethod
    def encode():
        pass

    @staticmethod
    def decode():
        pass


def matrix_to_image(array):
    return Image.fromarray(array)


def image_to_matrix(file_path):
    return np.array(Image.open(file_path))
