from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re
from Crypto.Cipher import AES

ppmPicture = "./CTR.ppm"
im = Image.open('./CTR.jpeg')
im.save(ppmPicture)

input = ppmPicture
output = open("out_ctr_dec.ppm","wb")
output.close()
output = open("out_ctr_dec.ppm",'ab')
line_count = 0
key = b'MORECOFFEEPLEASE'
nounce = b',\xd5{\xe95\x86B\xa1'
cipher = AES.new(key, AES.MODE_ECB)

def make_iv(n,cnt):
    tmp_iv = bytearray(16)
    for i in range(16):
        if i < 8:
            tmp_iv[i]=n[i]
        else:
            tmp_iv[i]=cnt[i-8]
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
counter_bytes= counter.to_bytes(8,'big')

initial_vector = make_iv(nounce,counter_bytes)
with open(input, 'rb') as f:
    while True:
        buf = f.read(16)
        if counter ==0:
            output.write(buf)
        else:
            msg=cipher.encrypt(initial_vector)
            decipher_text = bxor(msg,buf) 
            output.write(decipher_text)
        counter += 1
        initial_vector = make_iv(nounce,counter.to_bytes(8,'big'))
        if not buf:
            break

# Convert to jpeg
ppmPicture = "./out_ctr_dec.ppm"
im = Image.open(ppmPicture)
im.save("ctr_dec.jpeg")
