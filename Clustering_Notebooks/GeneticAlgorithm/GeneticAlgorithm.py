import configparser
import random
import pandas as pd
from dist_util import distance_map
from maulnik_ga import *
import time
NUMBER_OF_GENERATIONS = None
NUMBER_OF_MINIMUM = None


DISTANCE_MAP = distance_map()


STATE_DICT = {}

# def GeneticAlgorithm(k):
#     print("starting iteration: ", k)
#     if k > NUMBER_OF_GENERATIONS:
#         return
#
#     past_generation = STATE_DICT.get(k-1)
#     next_generation = []
#
#     while len(next_generation) < NUMBER_OF_MINIMUM:
#         # print("size of next generation:", len(next_generation))
#         sampling = random.sample(past_generation, 3)
#         state_1 = sampling[0]
#         state_2 = sampling[1]
#         state_3 = sampling[2]
#
#         new_state_1 = state_1.selection(state_2)
#
#         if new_state_1 is not None and new_state_1.isvalid():
#             next_generation.append(new_state_1)
#
#         new_state_1, new_state_2 = state_2.crossover(state_3, 1)
#         if new_state_1.isvalid():
#             next_generation.append(new_state_1)
#         if new_state_2.isvalid():
#             next_generation.append(new_state_2)
#
#         new_state_1, new_state_2 = state_3.mutation()
#         if new_state_1.isvalid():
#             next_generation.append(new_state_1)
#         if new_state_2.isvalid():
#             next_generation.append(new_state_2)
#
#         state_1.re_center()
#
#     STATE_DICT.update({k: next_generation})
#     GeneticAlgorithm(k+1)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('GA_config_5Cluster_L_inf.ini')

    # GENERAL PARAMETERS
    DATA_FILE = str(conf['GENERAL']['DATA_FILE'])
    SEED = int(conf['GENERAL']['SEED'])
    OUTPUT_FILE = str(conf['GENERAL']['OUTPUT_FILE'])
    random.seed(SEED)

    # CLUSTERING PARAMETERS
    DISTANCE_METRIC = str(conf['CLUSTERING']['DISTANCE_METRIC'])
    POINTS = int(conf['CLUSTERING']['POINTS'])
    DIMENSIONS = int(conf['CLUSTERING']['DIMENSION'])
    CLUSTERS = int(conf['CLUSTERING']['CLUSTERS'])
    DISTANCE_METRIC_FUNC = DISTANCE_MAP.get(DISTANCE_METRIC)

    # GA PARAMETERS
    INITIAL_POPULATION = int(conf['GA']['INITIAL_POPULATION'])
    NUMBER_OF_GENERATIONS = int(conf['GA']['NUMBER_OF_GENERATIONS'])
    NUMBER_OF_MINIMUM = int(conf['GA']['NUMBER_OF_MINIMUM'])
    MUTATION_RATE = float(conf['GA']['MUTATION_RATE'])

    df = pd.read_csv(DATA_FILE)
    arr = df.values

    max_value = arr.max()
    min_value = arr.min()

    POINTS_LIST = []
    for k in arr:
        initial = random.randint(1, CLUSTERS)
        p = Point(k)
        POINTS_LIST.append(p)

    chromosomes_pool = []

    chromosomes_count = DIMENSIONS*CLUSTERS
    for _ in range(4*chromosomes_count):
        chromosomes_pool.append(random.uniform(min_value, max_value))

    generation = []
    while len(generation) < INITIAL_POPULATION:
        selected = random.sample(range(len(chromosomes_pool)), chromosomes_count)
        chromosome_set = copy.deepcopy(chromosomes_pool)
        selected_chromosomes = [chromosome_set[x] for x in selected]

        points = copy.deepcopy(POINTS_LIST)
        new_state = State(points, selected_chromosomes,
                          CLUSTERS, DIMENSIONS,
                          MUTATION_RATE, DISTANCE_METRIC_FUNC)
        if new_state.isvalid():
            generation.append(new_state)
    start_time = time.time()
    print("Starting")
    GA_MODEL = GeneticAlgorithm(per_generation=NUMBER_OF_MINIMUM, generations=NUMBER_OF_GENERATIONS)
    GA_MODEL.seed_0(generation)
    GA_MODEL.fit()
    fittest = GA_MODEL.get_fittest()
    print("Done")
    elapsed_time = time.time() - start_time
    elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print("Time to complete:", elapsed)

    output_df = pd.DataFrame.from_records([s.to_dict() for s in fittest.points])
    output_df.to_csv(OUTPUT_FILE, index=False)
