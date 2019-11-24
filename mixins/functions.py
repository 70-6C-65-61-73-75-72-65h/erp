
def get_random_float_tax(value):
    """ markup_price ....."""
    return random.choice(np.arange(value[0], value[1], 0.1)) # 10 kop minimum

def get_random_float(value):
    return random.choice(np.arange(value[0], value[1], 0.1)) # 10 kop minimum

def get_random_int(value):
    return random.choice(range(value[0], value[1], 1))