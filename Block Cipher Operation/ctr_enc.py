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

# print(len(bin_data))
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from bitstring import BitArray

t = open(tmpPic,"wb")
t.write(bin_data)


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

# Randomly generate a nounce
nounce = b',\xd5{\xe95\x86B\xa1'
# print(nounce)

# Initialize counter
counter = 0
counter_bytes= counter.to_bytes(8,'big')

# Initialize nounce
initial_vector = make_iv(nounce,counter_bytes)

# divide plaintext into 16-byte blocks
plain_text_blocks=[]
with open(tmpPic, 'rb') as f:
    while True:
        buf = f.read(16)
        plain_text_blocks.append(buf)
        if not buf:
            break


key = b'MORECOFFEEPLEASE'
cipher = AES.new(key, AES.MODE_ECB)
output = open("out_ctr_enc.ppm","wb")
output.close()
output = open("out_ctr_enc.ppm","ab")
for i in range(len(plain_text_blocks)):
    if i==0:
        output.write(plain_text_blocks[i])
    else:
        msg=cipher.encrypt(initial_vector)
        msg_bin = BitArray(hex=msg.hex()).bin
        cipher_text_block = bxor(msg,plain_text_blocks[i])
        output.write(cipher_text_block)
    counter += 1
    initial_vector = make_iv(nounce,counter.to_bytes(8,'big'))
    # print(initial_vector.hex())

# Convert to jpeg
ppmPicture = "./out_ctr_enc.ppm"
im = Image.open(ppmPicture)
im.save("ctr_enc.jpeg")
    
#remove tmp file
import os
if os.path.exists("tmp.ppm"):
  os.remove("tmp.ppm")
