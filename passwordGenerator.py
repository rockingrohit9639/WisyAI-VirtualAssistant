import string
import random
def password_gen():
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation
    plen = int(input("Enter password length : "))
    # print(s1, s2, s3, s4)
    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))
    random.shuffle(s)
    password = "".join(s[0:plen])
    return password