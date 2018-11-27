import numpy as np


def l_1(pi, cj):
    diff = np.absolute(np.subtract(pi, cj))
    return np.sum(diff)


def l_inf(pi, cj):
    diff = np.abs(np.subtract(pi, cj))
    return np.max(diff)


def l_2(pi, cj):
    square = np.vectorize(lambda x: x**2)
    diff = np.absolute(np.subtract(pi, cj))
    return np.sum(square(diff))


def distance_map():
    return {'l_1': l_1,
            'l_inf': l_inf,
            'l_2': l_2
            }

