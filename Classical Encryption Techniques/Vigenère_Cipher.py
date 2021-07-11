# Vigenère Cipher

while True:

    try:
        #input
        key = input().lower()
        plaintext = input().lower()

        #new key
        new_key = ""
        for i in range((len(plaintext)//len(key)) + 1):
            new_key += key
        new_key = new_key[:len(plaintext)]

        #letter to number
        key_int = []
        for character in new_key:
            number = ord(character) - 97
            key_int.append(number)

        plaintext_int = []
        for character in plaintext:
            number = ord(character) - 97
            plaintext_int.append(number)

        ciphertext_int = []
        count = 0
        for num in plaintext_int:
            ciphertext_int.append((num+key_int[count]) % 26)
            count += 1

        #number to letter
        ciphertext = ""
        for number in ciphertext_int:
            character = chr(number+97)
            ciphertext += (character)

        #output
        print(ciphertext)

    except:
        break
