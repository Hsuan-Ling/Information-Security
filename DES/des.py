# DES

import string

def hex_toBinary(hex):

    binary = bin(int(hex, 16))[2:]

    #leading zeros
    length = len(hex)*4
    while ((len(binary)) < length):
        binary = '0' + binary

    return binary


def dec_toBinary(dec):

    binary = bin(dec)[2:]

    #leading zeros
    length = 4
    while ((len(binary)) < length):
        binary = '0' + binary

    return binary


def bin_toHex(bin):

    result = ""
    length = int(len(bin)/4)
    for i in range(0, length):
        result += hex(int(bin[i*4:i*4+4], 2))[2:].zfill(1)

    return result

def ascii_toBinary(string):
    
    binary = ""
    for c in string:
        character = bin(ord(c))[2:]
        while ((len(character)) < 8):
            character = '0' + character
        binary += character

    return binary

def permute(input, table):
    permutaion = ""
    for i in range(0, len(table)):
        permutaion += input[table[i]-1]
    return permutaion

def shift_left(input, nth_shifts):
    result = ""
    for i in range(nth_shifts):
        for j in range(1, len(input)):
            result += input[j]
        result += input[0]
        input = result
        result = ""
    return input

def xor(a, b):
    result = ""
    for i in range(len(a)):
        if a[i] != b[i]:
            result += "1"
        else: 
            result += "0"

    return result

# Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

# Expansion Table
expansion = [32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9, 
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]

# Straight Permutaion Table
per = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutaion Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]


# Permuted choice 1
pc1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Permuted choice 2
pc2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

def encrypt(plaintext, key):

    # Key generation
    # 1. Permuted choice 1: 64 to 56 bits
    key = permute(key, pc1)

    # 2. Spilting key
    left_key = key[0:28]
    right_key = key[28:56]

    # 3. Subkeys for 16 rounds
    subkeys = []
    for i in range(0, 16):
        # Shift
        left_key = shift_left(left_key, shift_table[i])
        right_key = shift_left(right_key, shift_table[i])

        # Permuted choice 2: 56 to 48 bits
        shifted_key = left_key + right_key
        shifted_key = permute(shifted_key, pc2)
        subkeys.append(shifted_key)

    # Encryption
    # Initial permutation
    plaintext = permute(plaintext, initial_perm)

    # Spilting plaintext
    left_pt = plaintext[0:32]
    right_pt = plaintext[32:64]

    for i in range(0, 16):

        # The Feistel (F)
        # 1. Expansion: 32 to 48 bits
        right_expanded = permute(right_pt, expansion)
        
        # 2. Key mixing
        xor_right = xor(right_expanded, subkeys[i])

        # 3. Substitution
        substitution = ""
        for j in range(0, 8):
            row = int((xor_right[j*6] + xor_right[j*6 + 5]), 2)
            col = int((xor_right[j*6 + 1] + xor_right[j*6 + 2] +
                      xor_right[j*6 + 3] + xor_right[j*6 + 4]), 2)
            substitution += dec_toBinary(sbox[j][row][col])


        # 4. Permutation
        substitution = permute(substitution, per)

        # XOR left and F's output
        result = xor(left_pt, substitution)
        left_pt = result

        # Swap left and right
        if(i != 15):
            tmp = left_pt
            left_pt = right_pt
            right_pt = tmp


    # Final permutation after 16 rounds
    combine = left_pt + right_pt
    ciphertext = permute(combine, final_perm)

    return ciphertext

while True:

    try:
        # input
        key = input()
        plaintext = input()

        # hex-key to binary
        key = hex_toBinary(key)

        # Padding
        # ????????????????????? block size ?????????
        # ?????????????????? (' ') ????????????????????????
        while ((len(plaintext)) % 8  != 0):
            plaintext += ' '

        # ECB mode
        # ?????????????????????????????????????????????
        plaintext_blocks = []
        plaintext_ascii = ascii_toBinary(plaintext)
        for i in range(int(len(plaintext_ascii)/64)):
            plaintext_blocks.append(plaintext_ascii[i*64:i*64+64])

        # Encrypt
        ans = ""
        for data in plaintext_blocks:
            ans += encrypt(data, key)

        # output
        print(bin_toHex(ans))

    except:
        break

