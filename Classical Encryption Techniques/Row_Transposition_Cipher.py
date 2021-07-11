# Row Transposition Ciphers

while True:

    try:
        #input
        key = input()
        plaintext = input()

        plaintext = plaintext.replace(" ", "")

        message = []
        
	for e in plaintext:
		message.append(e)

        ciphertext_list = []
        
        for i in range(len(key)):
            col = ""
            for j in range(len(plaintext)):
                if (j) % len(key) == i:
                    col += plaintext[j]
            ciphertext_list.append(col)

        ciphertext = ""
        for i in range(len(key)):
            idx = 0
            for num in key:
                if int(num) == (i+1):
                    ciphertext += ciphertext_list[idx]
                idx += 1

        #output
        print(ciphertext.lower())

    except:
        break
