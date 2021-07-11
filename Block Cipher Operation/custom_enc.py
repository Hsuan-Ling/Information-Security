import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import re
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Convert to ppm
ppmPicture = "./linux.ppm"
im = Image.open('./linux.jpeg')
im.save(ppmPicture)
tmpPic = "./tmp.ppm"

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


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

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
im.save("custom_enc.jpeg")


#remove tmp file
if os.path.exists("tmp.ppm"):
  os.remove("tmp.ppm")
