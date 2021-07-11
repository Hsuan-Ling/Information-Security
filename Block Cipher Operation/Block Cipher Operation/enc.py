#!/usr/bin/env python3
from bitstring import BitArray
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import sys

pic_file = sys.argv[1]
mode = sys.argv[2]

# Convert to ppm
ppmPicture = "./input_enc.ppm"
im = Image.open(sys.argv[1])
im.save(ppmPicture)
tmpPic = "./tmp.ppm"


def ecb(ppmPicture):

    # Read ppm as a binary file
    bin_data = open(ppmPicture, 'rb').read()

    t = open(tmpPic, "wb")

    key = b'MORECOFFEEPLEASE'
    cipher = AES.new(key, AES.MODE_ECB)

    # Add null bytes
    while (len(bin_data) % 16 != 0):
        bin_data += b'\x00'

    t.write(bin_data)
    # clear output
    output = open("out_ecb_enc.ppm", "wb")
    output.close()

    output = open("out_ecb_enc.ppm", 'ab')
    line_count = 0

    with open(tmpPic, 'rb') as f:
        while True:
            buf = f.read(16)
            if line_count == 0:
                msg = buf
            else:
                msg = cipher.encrypt(buf)
            output.write(msg)
            line_count += 1
            if not buf:
                break

    # Convert to jpeg
    Picture = "./out_ecb_enc.ppm"
    im = Image.open(Picture)
    im.save("./test_enc/ECB.jpeg")


def ctr(ppmPicture):

    # Read ppm as a binary file
    bin_data = open(ppmPicture, 'rb').read()
    t = open(tmpPic, "wb")


    t.write(bin_data)


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

    # Randomly generate a nounce
    nounce = b',\xd5{\xe95\x86B\xa1'
    
    # Initialize counter
    counter = 0
    counter_bytes = counter.to_bytes(8, 'big')

    # Initialize nounce
    initial_vector = make_iv(nounce, counter_bytes)

    # divide plaintext into 16-byte blocks
    plain_text_blocks = []
    with open(tmpPic, 'rb') as f:
        while True:
            buf = f.read(16)
            if buf != b'':
                plain_text_blocks.append(buf)
            if not buf:
                break


    key = b'MORECOFFEEPLEASE'
    cipher = AES.new(key, AES.MODE_ECB)
    output = open("out_ctr_enc.ppm", "wb")
    output.close()
    output = open("out_ctr_enc.ppm", "ab")
    for i in range(len(plain_text_blocks)):
        if i == 0:
            output.write(plain_text_blocks[i])
        else:
            msg = cipher.encrypt(initial_vector)
            msg_bin = BitArray(hex=msg.hex()).bin
            cipher_text_block = bxor(msg, plain_text_blocks[i])
            output.write(cipher_text_block)
        counter += 1
        initial_vector = make_iv(nounce, counter.to_bytes(8, 'big'))

    # Convert to jpeg
    Picture = "./out_ctr_enc.ppm"
    im = Image.open(Picture)
    im.save("./test_enc/CTR.jpeg")


def custom(ppmPicture):

    def byte_xor(ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    # Read ppm as a binary file
    bin_data = open(ppmPicture, 'rb').read()

    t = open(tmpPic, "wb")
    key1 = b'MORECOFFEEPLEASE'
    key2 = b'NOTHINGCANHELPME'

    # key2循環左移
    def make_key2(key):
        tmp_iv = bytearray(16)
        for i in range(16):
            if i < 15:
                tmp_iv[i] = key[i+1]
            else:
                tmp_iv[i] = key[0]
        return tmp_iv

    cipher = AES.new(key1, AES.MODE_ECB)

    # Add null bytes
    while (len(bin_data) % 16 != 0):
        bin_data += b'\x00'

    t.write(bin_data)
    # clear output
    output = open("out_custom_enc.ppm", "wb")
    output.close()

    output = open("out_custom_enc.ppm", 'ab')
    line_count = 0

    with open(tmpPic, 'rb') as f:
        while True:
            buf = f.read(16)
            if line_count == 0:
                msg = buf
            else:
                #對key2加密
            	 key2 = cipher.encrypt(key2)
            	 #加密後的key2和明文xor
            	 buf = byte_xor(buf, key2)
            	 #對處理後的明文加密
            	 msg = cipher.encrypt(buf)
            	 #key2循環左移
            	 key2 = make_key2(key2)
            output.write(msg)
            line_count += 1
            if not buf:
                break

    # Convert to jpeg
    ppmPicture = "./out_custom_enc.ppm"
    im = Image.open(ppmPicture)
    im.save("./test_enc/Custom.jpeg")

if(mode=="ECB"):
    ecb(ppmPicture)
elif(mode=="CTR"):
    ctr(ppmPicture)
elif(mode=="CUSTOM"):
    custom(ppmPicture)
else:
    print("./enc.py {filename}.jpeg {mode}(ECB,CTR,CUSTOM)")
