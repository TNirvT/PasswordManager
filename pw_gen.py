import string
from random import choice, randint, sample

# basic password generator
def pwgen_old():
    characters = string.ascii_letters + string.punctuation  + string.digits
    #print(characters)
    password =  "".join(choice(characters) for x in range(randint(8, 12)))
    return password

# modified *safer password generator
# contains 10 - 14 strings, with (1)cap, (2)small letter, (3) number, (4)1~3 punctuation
def pwgen():
    pw_length = randint(10,14)
    p_up = "".join(choice(string.ascii_uppercase) for x in range(randint(1,3)))
    p_nums = "".join(choice(string.digits) for x in range(randint(2,3)))
    p_punc = "".join(choice(string.punctuation) for x in range(randint(1,3)))
    p_low = "".join(choice(string.ascii_lowercase) for x in range(pw_length-len(p_up)-len(p_nums)-len(p_punc)))
    password = "".join(sample(p_up+p_low+p_nums+p_punc, pw_length))
    return password