import numpy as np
import pandas as pd
import configparser
import copy
import sys
from Point import *
from collections import Counter
import math
import random
import time

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


def l_1(pi, cj):
    diff = np.absolute(np.subtract(pi, cj))
    return np.sum(diff)


def l_infty(pi, cj):
    diff = np.abs(np.subtract(pi,cj))
    return np.max(diff)


def l_2(pi, cj):
    square = np.vectorize(lambda x: x**2)
    diff = np.absolute(np.subtract(pi, cj))
    return math.sqrt(np.sum(square(diff)))


def count_occurrence(points_list):
    count_map = {}
    for point in points_list:
        assignment = point.assignment
        if count_map.get(assignment) is not None:
            count_map[assignment] = count_map.get(assignment)+1
        else:
            count_map[assignment] = 1
    return count_map


DISTANCE_METRICS = {'L_1': l_1,
                    'L_INF': l_infty,
                    'L_2': l_2}

DISTANCE = None


def calculate_score(POINTS_LIST, clusters):
    total = 0
    for k in range(1, clusters+1):
        ls = list(filter(lambda x: x.get_assignment() == k, POINTS_LIST))
        if len(ls)>0:
            matrix = np.vstack(list(map(lambda x: x.dimension, ls)))
            median = np.median(matrix, axis=0)

            total += sum(map(lambda x: DISTANCE(x.dimension, median), ls))

    return total


def additive_step_function(temperature, step):
    return temperature-step


def percent_step_function(temperature, step):
    return temperature*(1-step)


step_function = {"ADDITIVE": additive_step_function,
                 "PERCENT": percent_step_function}

STEP_FUNCTION = None


def sa_algorithm(POINTS_LIST):
    current_temp = MAX_TEMP
    min_state = copy.deepcopy(POINTS_LIST)
    minimization = calculate_score(min_state, CLUSTERS)

    while current_temp > .1:
        print("Current Temperature: " + str(current_temp))
        for _ in range(NUMBER_PER_ADJUSTMENT):
            modified = []
            occ_map = count_occurrence(POINTS_LIST)
            random_sampling = random.sample(range(POINTS), k=NUMBER_OF_SWAPS)
            for pi in random_sampling:
                point = POINTS_LIST[pi]
                current_cluster = point.get_assignment()
                occ = occ_map.get(current_cluster)
                if occ is None or occ < 2:
                    print(current_temp, occ)
                    continue

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
                    print("hello ")
                    min_state = copy.deepcopy(POINTS_LIST)

            elif random_v < prob:
                minimization = score
                map(lambda x: POINTS_LIST[x].update(), modified)

            else:
                map(lambda x: POINTS_LIST[x].reset(), modified)

        current_temp = STEP_FUNCTION(current_temp, TEMP_STEP_SIZE)

    return min_state, minimization


if __name__ == '__main__':
    conf_file = sys.argv[1]
    conf = configparser.ConfigParser()
    conf.read(conf_file)

    DATA_FILE = str(conf['GENERAL']['DATA_FILE'])
    OUTPUT_FILE = str(conf['GENERAL']['OUTPUT_FILE'])
    SEED = int(conf['GENERAL']['SEED'])

    DISTANCE_METRIC = str(conf['CLUSTERING']['DISTANCE_METRIC'])
    POINTS = int(conf['CLUSTERING']['POINTS'])
    DIMENSIONS = int(conf['CLUSTERING']['DIMENSION'])
    CLUSTERS = int(conf['CLUSTERING']['CLUSTERS'])

    MAX_TEMP = int(conf['SA']['MAX_TEMP'])
    STEP_FUNCTION_TYPE = str(conf['SA']['STEP_FUNCTION'])
    TEMP_STEP_SIZE = float(conf['SA']['TEMP_STEP'])
    NUMBER_OF_SWAPS = int(conf['SA']['NUMBER_OF_SWAPS'])
    NUMBER_PER_ADJUSTMENT = int(conf['SA']['NUMBER_PER_ADJUSTMENT'])

    STEP_FUNCTION = step_function[STEP_FUNCTION_TYPE]

    random.seed(SEED)

    df = pd.read_csv(DATA_FILE)
    # df = df.drop("species", axis=1)
    arr = df.values

    DISTANCE = DISTANCE_METRICS[DISTANCE_METRIC]

    POINTS_LIST = []
    row_id = 0
    for k in arr:
        initial = random.randint(1, CLUSTERS)
        p = Point(row_id, k, initial)
        POINTS_LIST.append(p)
        row_id += 1

    start_time = time.time()
    print("Starting Fit")
    state, min_value = sa_algorithm(POINTS_LIST)
    print("min value", min_value)
    output_df = pd.DataFrame.from_records([s.to_dict() for s in state])
    output_df.to_csv(OUTPUT_FILE, index=False)
    print("Minimum Cost Function:" + str(min_value))
    elapsed_time = time.time() - start_time
    elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print("Time to complete:", elapsed)
