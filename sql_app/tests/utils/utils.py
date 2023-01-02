import random
import string
N = 10

def random_string():
    return ''.join(random.choices(string.ascii_lowercase, k=N))

def random_email():
    num = random.randint(1, 10000)
    return f'artem{num}@gamil.com'
