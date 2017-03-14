import random
import string
import secrets


# generates a random string with specified length
def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


# generates a random int, with optional range
def random_int(min=0, max=9999999999):
    return random.randint(min, max)


# generates a cryptographic url-safe token
def generate_token():
    token = secrets.token_urlsafe(32)
    return token
