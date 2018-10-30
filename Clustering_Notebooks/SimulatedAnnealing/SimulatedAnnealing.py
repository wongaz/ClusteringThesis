import numpy as np
import pandas as pd
import configparser
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


def naive_brute_force(POINTS_LIST):
    def nested(index, points):
        if index == POINTS:
            array = [o.get_assignment() for o in POINTS_LIST]
            #print(array)
            counts = Counter(array)
            for k in range(1, CLUSTERS+1):
                #print(k, counts.get(k))
                if counts.get(k) == 0 or counts.get(k) is None:
                    return
            score = calculate_score(POINTS_LIST, CLUSTERS)

            global best, best_assignment
            if score < best:
                best = score
                best_assignment = array
                print(best,best_assignment)
            return
        else:
            for k in range(1, CLUSTERS+1):
                points[index].set_assignment(k)
                nested(index+1, POINTS_LIST)

    nested(0, POINTS_LIST)
    return best,best_assignment


def SA_Algorithm(POINTS_LIST):
    current_temp = MAX_TEMP
    minimization = calculate_score(POINTS_LIST,CLUSTERS)

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
            diff = score - minimization
            prob = math.exp((-diff)/ round(current_temp, 10))
            random_v = random.random()
            print(current_temp, modified, minimization, score, diff, prob, random_v)

            if score <= minimization or random_v < prob:
                minimization = score
                map(lambda x: POINTS_LIST[x].update(), modified)

            else:
                map(lambda x: POINTS_LIST[x].reset(), modified)

        current_temp-=TEMP_STEP_SIZE

    return minimization


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
    print(naive_brute_force(POINTS_LIST))
    #print(SA_Algorithm(POINTS_LIST))
