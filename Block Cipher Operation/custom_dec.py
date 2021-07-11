from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import re
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


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
            #解密key2
            key2 = decipher.encrypt(key2)
            #解密密文
            msg = decipher.decrypt(buf)
            #兩者xor
            msg = byte_xor(msg, key2)
            #key2循環左移
            key2 = make_key2(key2)
        output.write(msg)
        line_count += 1
        if not buf:
            break

# Convert to jpeg
ppmPicture = "./out_custom_dec.ppm"
im = Image.open(ppmPicture)
im.save("custom_dec.jpeg")
