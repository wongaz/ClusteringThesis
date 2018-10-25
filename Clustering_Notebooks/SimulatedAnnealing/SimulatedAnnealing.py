import numpy as np
import pandas as pd
import configparser
from Point import *
import math
import random

DISTANCE_METRIC = None
POINTS = None
DIMENSIONS = None
CLUSTERS = None

MAX_TEMP = None
TEMP_STEP_SIZE = None

def L_1(pi, cj):
    diff = np.absolute(np.subtract(pi, cj))
    return np.sum(diff)


def L_INF(pi, cj):
    diff = np.abs(np.subtract(pi,cj))
    return np.max(diff)


DISTANCE_METRICS = {'L_1': L_1,
                   'L_INF': L_INF}

DISTANCE = None


def calculate_score(POINTS_LIST):
    total = 0
    for k in range(1,CLUSTERS+1):
        ls = list(filter(lambda x: x.get_assignment() == k, POINTS_LIST))
        matrix = np.vstack(list(map(lambda x: x.dimension, ls)))
        median = np.median(matrix, axis=0)

        total += sum(map(lambda x: DISTANCE(x.dimension, median), ls))

    return total


def SA_Algorithm(POINTS_LIST):
    current_temp = MAX_TEMP
    best = calculate_score(POINTS_LIST)

    while current_temp > 1:
        pi = random.randrange(POINTS)
        cj = random.randint(1, CLUSTERS)
        while POINTS_LIST[pi].set_next(cj) is False:
            cj = random.randint(1, CLUSTERS)

        score = calculate_score(POINTS_LIST)
        diff = math.exp(-(best - score / round(current_temp, 10)))
        random_v = random.random()
        print(current_temp,best,score, diff, random_v)

        if score<best or diff < random_v:
            best = score
            POINTS_LIST[pi].update()

        else:
            POINTS_LIST[pi].reset()

        current_temp-=TEMP_STEP_SIZE

    return best


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    DATA_FILE = str(conf['GENERAL']['DATA_FILE'])
    SEED = int(conf['GENERAL']['SEED'])

    DISTANCE_METRIC = str(conf['CLUSTERING']['DISTANCE_METRIC'])
    POINTS = int(conf['CLUSTERING']['POINTS'])
    DIMENSIONS = int(conf['CLUSTERING']['DIMENSION'])
    CLUSTERS = int(conf['CLUSTERING']['CLUSTERS'])

    MAX_TEMP = int(conf['SA']['MAX_TEMP'])
    TEMP_STEP_SIZE = float(conf['SA']['TEMP_STEP'])

    df = pd.read_csv(DATA_FILE)
    arr = df.values

    DISTANCE = DISTANCE_METRICS[DISTANCE_METRIC]

    POINTS_LIST = []
    for k in arr:
        initial = random.randint(1, CLUSTERS)
        p = Point(k, initial)
        POINTS_LIST.append(p)

    print(SA_Algorithm(POINTS_LIST))
