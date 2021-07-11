# Caesar cipher

while True:

    try:
        #input
        plaintext = input().lower()
        key = 9

        #letter to number
        plaintext_int = []
        for character in plaintext:
            number = ord(character) - 97
            plaintext_int.append(number)

        ciphertext_int = []
        for num in plaintext_int:
            if num >= 0 and num <= 25 :
                ciphertext_int.append((num+key) % 26)
            else:
                #非字母不做處理直接輸出
                ciphertext_int.append(num)
            
            

        #number to letter
        ciphertext = ""
        for number in ciphertext_int:
            character = chr(number+97)
            ciphertext += (character)

        #output
        print(ciphertext)

    except:
        break
