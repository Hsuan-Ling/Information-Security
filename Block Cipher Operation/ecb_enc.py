from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re

# Convert to ppm
ppmPicture = "./linux.ppm"
im = Image.open('./linux.jpeg')
im.save(ppmPicture)
tmpPic = "./tmp.ppm"

# Read ppm as a binary file 
bin_data = open(ppmPicture, 'rb').read()
# print(len(bin_data))

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

t = open(tmpPic,"wb")
key = b'MORECOFFEEPLEASE'
cipher = AES.new(key, AES.MODE_ECB)

# Add null bytes
while (len(bin_data)%16!=0):
    bin_data += b'\x00'
    # print(len(bin_data))

t.write(bin_data)
# clear output
output = open("out_ecb_enc.ppm","wb")
output.close()

output = open("out_ecb_enc.ppm",'ab')
line_count = 0

with open(tmpPic, 'rb') as f:
    while True:
        buf = f.read(16)
        if line_count ==0:
            msg = buf
        else:
            msg=cipher.encrypt(buf)
        output.write(msg)
        line_count += 1
        if not buf:
            break

# Convert to jpeg
ppmPicture = "./out_ecb_enc.ppm"
im = Image.open(ppmPicture)
im.save("ecb_enc.jpeg")


#remove tmp file
import os
if os.path.exists("tmp.ppm"):
  os.remove("tmp.ppm")
