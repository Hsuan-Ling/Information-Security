# Playfair cipher

import string
import itertools


def chunker(seq, size):
    it = iter(seq)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


def prepare_input(dirty):

    # up-casing
    dirty = "".join([c.upper() for c in dirty if c in string.ascii_letters])
    clean = ""

    if len(dirty) < 2:
        return dirty

    for i in range(len(dirty) - 1):
        clean += dirty[i]

        # if repeat, separat with X
        if dirty[i] == dirty[i + 1]:
            clean += "Z"

    clean += dirty[-1]

    if len(clean) & 1:
        clean += "Z"

    return clean


def generate_table(key):

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    table = []

    # key to the table
    for char in key.upper():
        if char not in table and char in alphabet:
            table.append(char)

    # fill the table
    for char in alphabet:
        if char not in table:
            table.append(char)

    return table


def encode(plaintext, key):
    table = generate_table(key)
    plaintext = prepare_input(plaintext)
    ciphertext = ""

    for char1, char2 in chunker(plaintext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)

        if row1 == row2:
            ciphertext += table[row1 * 5 + (col1 + 1) % 5]
            ciphertext += table[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += table[((row1 + 1) % 5) * 5 + col1]
            ciphertext += table[((row2 + 1) % 5) * 5 + col2]
        else:
            ciphertext += table[row1 * 5 + col2]
            ciphertext += table[row2 * 5 + col1]

    return ciphertext


while True:

    try:
        #input
        key = input()
        plaintext = input()

        #output
        print(encode(plaintext, key))

    except:
        break
