# Rail Fence Cipher

while True:

    try:
        #input
        key = int(input())
        plaintext = input()

        ciphertext_matrix = [['\n' for j in range(len(plaintext))]
                for i in range(key)]


        dir_down = False
        row, col = 0, 0

        for i in range(len(plaintext)):

            if (row == 0) or (row == key - 1):
                dir_down = not dir_down

            ciphertext_matrix[row][col] = plaintext[i]
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        
        ciphertext = []
        for i in range(key):
            for j in range(len(plaintext)):
                if ciphertext_matrix[i][j] != '\n':
                    ciphertext.append(ciphertext_matrix[i][j])
        
        #output
        print("" . join(ciphertext))

    except:
        break
