import random
import string
N = 10

def random_string():
    return ''.join(random.choices(string.ascii_lowercase, k=N))

def random_email():
    return random_string() + '@' + random_string()[:5]
