# basic random pw algorithm

import string
from random import *

# basic password generator
def genpw():
    characters = string.ascii_letters + string.punctuation  + string.digits
    #print(characters)
    password =  "".join(choice(characters) for x in range(randint(8, 12)))
    return password

# To do: add another *safe password generator
# contains 8 - 12 strings, with (1)caps, (2)small letters, (3) numbers, (4)1 or 2 punctuation
# def gensafepw():
#     pw_length = [8,12]