
import random
import numpy as np
def get_random_float_tax(value):
    """ markup_price ....."""
    return random.choice(np.arange(value[0], value[1], 0.1)) # 10 kop minimum

def get_random_float(value):
    return random.choice(np.arange(value[0], value[1], 0.1)) # 10 kop minimum

def get_random_int(value):
    return random.choice(range(value[0], value[1], 1))

def get_binominal(ranges, prob):
    """ to first and second value of ids add  + 1"""
    return np.random.binomial(len(range(ranges[0], ranges[1])), prob) + ranges[0]

def get_float_binominal(ranges, prob):
    return float(get_binominal([int(ranges[0]*10), int(ranges[1]*10)], prob)/10)