import os
from bitstring import BitArray
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def ecb():

    input = "./out_ecb_enc.ppm"

    output = open("out_ecb_dec.ppm", "wb")
    output.close()
    output = open("out_ecb_dec.ppm", 'ab')
    line_count = 0
    key = b'MORECOFFEEPLEASE'
    decipher = AES.new(key, AES.MODE_ECB)

    with open(input, 'rb') as f:
        while True:
            buf = f.read(16)
            if line_count == 0:
                msg = buf
            else:
                msg = decipher.decrypt(buf)
            output.write(msg)
            line_count += 1
            if not buf:
                break

    # Convert to jpeg
    Picture = "./out_ecb_dec.ppm"
    im = Image.open(Picture)
    im.save("./test_dec/ECB.jpeg")


def ctr():

    input = "./out_ctr_enc.ppm"

    output = open("out_ctr_dec.ppm", "wb")
    output.close()
    output = open("out_ctr_dec.ppm", 'ab')
    line_count = 0
    key = b'MORECOFFEEPLEASE'
    nounce = b',\xd5{\xe95\x86B\xa1'
    cipher = AES.new(key, AES.MODE_ECB)


    def make_iv(n, cnt):
        tmp_iv = bytearray(16)
        for i in range(16):
            if i < 8:
                tmp_iv[i] = n[i]
            else:
                tmp_iv[i] = cnt[i-8]
        return tmp_iv

    # xor for bytes
    def bxor(b1, b2):
        result = b""
        for b1, b2 in zip(b1, b2):
            result += bytes([b1 ^ b2])
        return result


    # create a 16 byte array to hold IV
    initial_vector = bytearray(16)
    # Initialize nounce
    nounce = b',\xd5{\xe95\x86B\xa1'
    # Initialize counter
    counter = 0
    counter_bytes = counter.to_bytes(8, 'big')

    initial_vector = make_iv(nounce, counter_bytes)
    with open(input, 'rb') as f:
        while True:
            buf = f.read(16)
            if counter == 0:
                output.write(buf)
            else:
                msg = cipher.encrypt(initial_vector)
                decipher_text = bxor(msg, buf)
                output.write(decipher_text)
            counter += 1
            initial_vector = make_iv(nounce, counter.to_bytes(8, 'big'))
            if not buf:
                break

    # Convert to jpeg
    Picture = "./out_ctr_dec.ppm"
    im = Image.open(Picture)
    im.save("./test_dec/CTR.jpeg")


def custom():

    def byte_xor(ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    # key2循環左移
    def make_key2(key):
        tmp_iv = bytearray(16)
        for i in range(16):
            if i < 15:
                tmp_iv[i] = key[i+1]
            else:
                tmp_iv[i] = key[0]
        return tmp_iv


    input = "./out_custom_enc.ppm"
    output = open("out_custom_dec.ppm", "wb")
    output.close()
    output = open("out_custom_dec.ppm", 'ab')
    line_count = 0
    key1 = b'MORECOFFEEPLEASE'
    key2 = b'NOTHINGCANHELPME'
    decipher = AES.new(key1, AES.MODE_ECB)

    with open(input, 'rb') as f:
        while True:
            buf = f.read(16)
            if line_count == 0:
                msg = buf
            else:
                #key2 = decipher.encrypt(key2)
                msg = decipher.decrypt(buf)
                msg = byte_xor(msg, key2)
                key2 = make_key2(key2)
            output.write(msg)
            line_count += 1
            if not buf:
                break

    # Convert to jpeg
    Picture = "./out_custom_dec.ppm"
    im = Image.open(Picture)
    im.save("./test_dec/Custom.jpeg")

os.mkdir("test_dec")
ecb()
if os.path.exists("tmp.ppm"):
    os.remove("tmp.ppm")

ctr()
if os.path.exists("tmp.ppm"):
    os.remove("tmp.ppm")

custom()
if os.path.exists("tmp.ppm"):
    os.remove("tmp.ppm")
