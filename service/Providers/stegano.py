import cv2
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display


class LSB:

    def __init__(self, img_path):
        self.image = cv2.imread(img_path)
        self.height, self.width, self.channels = self.image.shape
        self.size = self.width * self.height

        self.current_width = 0
        self.current_height = 0
        self.current_channel = 0

        self.mask_zero_values = [254, 253, 251, 247, 239, 223, 191, 127]
        self.mask_one_values = [1, 2, 4, 8, 16, 32, 64, 128]
        self.mask_zero = self.mask_zero_values.pop(0)
        self.mask_one = self.mask_one_values.pop(0)

    def encode_msg(self, msg):
        msg_size = len(msg)
        bsize = self.binary_val(size=msg_size, bit_size=16)
        self.set_binary_val(bits=bsize)

        for char in msg:
            c = ord(char)
            self.set_binary_val(bits=self.binary_val(c, 16))
        return self.image

    def encode_image(self, img_path):
        encode_image = cv2.imread(img_path)
        img_height, img_width, img_channels = encode_image.shape

        if self.width * self.height * self.channels < img_height * img_width * img_channels:
            raise CustomException("Carrier image not big enough to hold all the data to steganography")

        bin_w = self.binary_val(img_width, 16)
        bin_h = self.binary_val(img_height, 16)
        self.set_binary_val(bin_w)
        self.set_binary_val(bin_h)

        for _h in range(img_height):
            for _w in range(img_width):
                for _c in range(img_channels):
                    val = encode_image[_h, _w][_c]
                    self.set_binary_val(self.binary_val(int(val), 8))

        return self.image

    def encode_binary(self, _data):
        len_data = len(_data)
        if self.width * self.height * self.channels < len_data + 64:
            raise CustomException("Carrier image not big enough to hold all the data to steganography")

        self.set_binary_val(self.binary_val(len_data, 64))
        for byte in _data:
            byte = byte if isinstance(byte, int) else ord(byte)
            self.set_binary_val(self.binary_val(byte, 8))

        return self.image

    def decode_msg(self):
        _bits = self.get_bits(bit_size=16)
        _byte = int(_bits, 2)
        i = 0
        _msg = ''
        while i < _byte:
            tmp = self.get_bits(bit_size=16)
            _msg += chr(int(tmp, 2))
            i += 1
        reshaped_text = arabic_reshaper.reshape(_msg)
        decode_msg = get_display(reshaped_text)
        return decode_msg

    def decode_image(self):
        _bits = self.get_bits(bit_size=16)
        diff_img = np.zeros((int(_bits, 2), int(_bits, 2), 3), np.uint8)
        _height, _width, _channels = diff_img.shape

        for h in range(_height):
            for w in range(_width):
                for c in range(_channels):
                    val = list(diff_img[h, w])
                    val[c] = int(self.get_bits(bit_size=8), 2)
                    diff_img[h, w] = tuple(val)

        return diff_img

    def decode_binary(self):
        len_byte = int(self.get_bits(bit_size=64), 2)

        _byte = b""
        for i in range(len_byte):
            _byte += chr(int(self.get_bits(bit_size=8), 2)).encode("utf-8")

        return _byte

    @staticmethod
    def binary_val(size, bit_size):
        bs = bin(size)[2:]
        if len(bs) > bit_size:
            raise CustomException('binary value larger than the expected size')

        while len(bs) < bit_size:
            bs = '0' + bs
        return bs

    def set_binary_val(self, bits):
        for c in bits:
            val = list(self.image[self.current_height, self.current_width])
            if int(c) == 1:
                val[self.current_channel] = int(val[self.current_channel]) | self.mask_one
            else:
                val[self.current_channel] = int(val[self.current_channel]) & self.mask_zero

            self.image[self.current_height, self.current_width] = tuple(val)
            self.next_slot()

    def next_slot(self):
        if self.current_channel == self.channels - 1:
            self.current_channel = 0
            if self.current_width == self.width - 1:
                self.current_width = 0
                if self.current_height == self.height - 1:
                    self.current_height = 0
                    if self.mask_one == 128:
                        raise CustomException("No available slot remaining (image filled)")
                    else:
                        self.mask_one = self.mask_one_values.pop(0)
                        self.mask_zero = self.mask_zero_values.pop(0)
                else:
                    self.current_height += 1
            else:
                self.current_width += 1
        else:
            self.current_channel += 1

    def get_bits(self, bit_size):
        bits = ''
        for i in range(bit_size):
            bits += self.get_bit()
        return bits

    def get_bit(self):
        val = self.image[self.current_height, self.current_width][self.current_channel]
        val = int(val) & self.mask_one
        self.next_slot()
        if val > 0:
            return "1"
        else:
            return "0"


class CustomException(Exception):
    pass
