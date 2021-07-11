from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


input = "./out_cbc_enc.ppm"
output = open("out_cbc_dec.ppm","wb")
output.close()
output = open("out_cbc_dec.ppm",'ab')
line_count = 0
key = b'MORECOFFEEPLEASE'
iv = b'NOTHINGCANHELPME'
decipher = AES.new(key, AES.MODE_ECB)

vector = iv

with open(input, 'rb') as f:
    while True:
        buf = f.read(16)
        if line_count ==0:
            msg = buf
        else:
            msg=decipher.decrypt(buf)
            msg = byte_xor(msg, vector)
            vector = buf
        output.write(msg)
        line_count += 1
        if not buf:
            break

# Convert to jpeg
ppmPicture = "./out_cbc_dec.ppm"
im = Image.open(ppmPicture)
im.save("cbc_dec.jpeg")
