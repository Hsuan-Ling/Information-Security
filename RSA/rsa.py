import random

def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)):
        if num % n == 0:
            return False
    return True


def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)


def generate_d(e, f):

    a = e
    b = f
    x1, x2 = 0, 1
    y1, y2 = 1, 0

    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        x2, x1 = x1, x2 - quotient * x1
        y2, y1 = y1, y2 - quotient * y1

    if (x2 < 0):
        return x2 + f
    else:
        return x2


def generate_keys(p, q):

    # p和q為質數
    if (is_prime(p) and is_prime(q)):

        # p is not equal to q
        if not p == q:

            # 計算n=pq
            n = p * q

            # 計算f(n)=(p-1)(q-1)
            f = (p-1) * (q-1)

            # 找一個隨機數e，且1<e<f(n)
            e = random.randrange(1, f)

            # 確保隨機數e與f(n)互質
            g = gcd(e, f)
            while g != 1:
                e = random.randrange(1, f)
                g = gcd(e, f)

            # generate d for private key
            d = generate_d(e, f)

            # public key is (e, n) and private key is (d, n)
            return ((e, n), (d, n))

        else: 
            print("p can't be equal to q")
            exit()
    else:
        print("p and q should both be prime")
        exit()


def encrypt(public_key, plaintext):

    e, n = public_key

    # plaintext 需小於 n=pq
    if(int(plaintext) < n):
        ciphertext = pow(int(plaintext), e, n)
        return ciphertext

    else:
        print("plaintext is too big")
        exit()


def decrypt(private_key, ciphertext):

    d, n = private_key
    plaintext = pow(int(ciphertext), d, n)

    return plaintext


p = int(input("Enter first prime number p: "))
q = int(input("Enter second prime number q: "))

public, private = generate_keys(p, q)

message = input("Enter the plaintext (less than p*q): ")
encrypted_msg = encrypt(public, message)

print("The encrypted number is: ", encrypted_msg)
print("The decrypted number is: ", decrypt(private, encrypted_msg))
