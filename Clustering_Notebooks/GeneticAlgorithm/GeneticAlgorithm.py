import configparser
import random
import pandas as pd
from dist_util import distance_map
from maulnik_ga import *

DISTANCE_MAP = distance_map()


def GeneticAlgorithm(initial_state):
    pass

if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('ga_config.ini')

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

    max_value = arr.max()
    min_value = arr.min()

    POINTS_LIST = []
    for k in arr:
        initial = random.randint(1, CLUSTERS)
        p = Point(k)
        POINTS_LIST.append(p)
    cluster = []
    for _ in range(CLUSTERS):
        arr = []
        for _ in range(DIMENSIONS):
            arr += random.uniform(min_value,max_value)

    #print(naive_brute_force(POINTS_LIST))
    print()