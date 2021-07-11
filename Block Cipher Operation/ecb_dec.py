from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
input = "./out_ecb_enc.ppm"
output = open("out_ecb_dec.ppm","wb")
output.close()
output = open("out_ecb_dec.ppm",'ab')
line_count = 0
key = b'MORECOFFEEPLEASE'
decipher = AES.new(key, AES.MODE_ECB)

with open(input, 'rb') as f:
    while True:
        buf = f.read(16)
        if line_count ==0:
            msg = buf
        else:
            msg=decipher.decrypt(buf)
        output.write(msg)
        line_count += 1
        if not buf:
            break

# Convert to jpeg
ppmPicture = "./out_ecb_dec.ppm"
im = Image.open(ppmPicture)
im.save("ecb_dec.jpeg")
