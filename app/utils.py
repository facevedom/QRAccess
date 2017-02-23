import random, string

# returns a random string with specified length
def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))