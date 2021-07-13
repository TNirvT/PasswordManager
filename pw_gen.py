import string
from random import choice, randint, sample

def phrase_gen(min_len, max_len):
    characters = string.ascii_letters + string.digits
    phrase =  "".join(choice(characters) for x in range(randint(min_len, max_len)))
    return phrase

# empty input: password with most punctuations choices
# punctuations-only input: password with these input choices
# mixed input: directly input password
def pwgen(in_put):
    in_put = str(in_put).replace(" ","")
    if in_put != "" and not __allpunct(in_put): return in_put
    pw_length = randint(10,14)
    p_up = "".join(choice(string.ascii_uppercase) for x in range(randint(1,3)))
    p_nums = "".join(choice(string.digits) for x in range(randint(2,3)))
    if in_put == "":
        p_punc = "".join(choice("!@#$%^&*-_+=<>,./?") for x in range(randint(1,3)))
    else:
        p_punc = "".join(choice(in_put) for x in range(randint(1,2)))
    p_low = "".join(choice(string.ascii_lowercase) for x in range(pw_length-len(p_up)-len(p_nums)-len(p_punc)))
    password = "".join(sample(p_up+p_low+p_nums+p_punc, pw_length))
    return password

def __allpunct(in_put):
    for i in in_put:
        if i not in string.punctuation:
            return False
    return True