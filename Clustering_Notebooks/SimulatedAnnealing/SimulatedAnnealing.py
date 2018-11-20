import numpy as np
import pandas as pd
import configparser
import copy
from Point import *
from collections import Counter
import math
import random

DISTANCE_METRIC = None
POINTS = None
DIMENSIONS = None
CLUSTERS = None
CLUSTER_MAP = {}

MAX_TEMP = None
TEMP_STEP_SIZE = None
NUMBER_OF_SWAPS = None
NUMBER_PER_ADJUSTMENT = None

best = math.inf
best_assignment = []


def L_1(pi, cj):
    diff = np.absolute(np.subtract(pi, cj))
    return np.sum(diff)


def L_INF(pi, cj):
    diff = np.abs(np.subtract(pi,cj))
    return np.max(diff)


DISTANCE_METRICS = {'L_1': L_1,
                   'L_INF': L_INF}

DISTANCE = None


def calculate_score(POINTS_LIST, clusters):
    total = 0
    for k in range(1, clusters+1):
        ls = list(filter(lambda x: x.get_assignment() == k, POINTS_LIST))
        matrix = np.vstack(list(map(lambda x: x.dimension, ls)))
        median = np.median(matrix, axis=0)

        total += sum(map(lambda x: DISTANCE(x.dimension, median), ls))

    return total


def additive_step_function(temper, step):
    return temper-step


def percent_step_function(temper, step):
    return temper*(1-step)


step_function = {"ADDITVE": additive_step_function,
                 "PERCENT": percent_step_function}


def sa_algorithm(POINTS_LIST):
    current_temp = MAX_TEMP
    min_state = copy.deepcopy(POINTS_LIST)
    minimization = calculate_score(min_state, CLUSTERS)

    while current_temp > .1:
        for _ in range(NUMBER_PER_ADJUSTMENT):
            modified = []
            for _ in range(NUMBER_OF_SWAPS):
                pi = random.randrange(POINTS)
                modified.append(pi)
                cj = random.randint(1, CLUSTERS)
                while POINTS_LIST[pi].set_next(cj) is False:
                    cj = random.randint(1, CLUSTERS)

            score = calculate_score(POINTS_LIST, CLUSTERS)
            diff = abs(score - minimization)
            prob = math.exp(-diff / round(current_temp, 10))
            random_v = random.random()

            if score <= minimization:
                minimization = score
                map(lambda x: POINTS_LIST[x].update(), modified)
                if score < calculate_score(min_state, CLUSTERS):
                    min_state = copy.deepcopy(POINTS_LIST)

            elif random_v < prob:
                minimization = score
                map(lambda x: POINTS_LIST[x].update(), modified)

            else:
                map(lambda x: POINTS_LIST[x].reset(), modified)

        current_temp -= TEMP_STEP_SIZE

    return min_state, minimization


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('sa_config.ini')

    DATA_FILE = str(conf['GENERAL']['DATA_FILE'])
    SEED = int(conf['GENERAL']['SEED'])

    DISTANCE_METRIC = str(conf['CLUSTERING']['DISTANCE_METRIC'])
    POINTS = int(conf['CLUSTERING']['POINTS'])
    DIMENSIONS = int(conf['CLUSTERING']['DIMENSION'])
    CLUSTERS = int(conf['CLUSTERING']['CLUSTERS'])

    MAX_TEMP = int(conf['SA']['MAX_TEMP'])
    TEMP_STEP_SIZE = float(conf['SA']['TEMP_STEP'])
    NUMBER_OF_SWAPS = int(conf['SA']['NUMBER_OF_SWAPS'])
    NUMBER_PER_ADJUSTMENT = int(conf['SA']['NUMBER_PER_ADJUSTMENT'])

    df = pd.read_csv(DATA_FILE)
    arr = df.values

    DISTANCE = DISTANCE_METRICS[DISTANCE_METRIC]

    POINTS_LIST = []
    for k in arr:
        initial = random.randint(1, CLUSTERS)
        p = Point(k, initial)
        POINTS_LIST.append(p)
    #print(naive_brute_force(POINTS_LIST))
    print(sa_algorithm(POINTS_LIST))
