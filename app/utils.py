import random, string

# returns a random string with specified length
def random_string(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))