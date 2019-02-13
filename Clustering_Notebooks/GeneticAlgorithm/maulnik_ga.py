import numpy as np
import random
import math
import copy
from dist_util import distance_map


class Point(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.assignment = None

    def __str__(self):
        return str(self.dimension) + " " + str(self.assignment)

    def set_assignment(self, val):
        self.assignment = val

    def to_dict(self):
        new_dict = dict()
        new_dict.update({"assignment": self.assignment})
        for k in range(len(self.dimension)):
            current_str = "x"+str(k+1)
            new_dict.update({current_str: self.dimension[k]})
        return new_dict


class Center(object):
    def __init__(self, dimension, label):
        self.dimension = dimension
        self.id = label
        self.fitness = None
        self.probability = 0

    def __str__(self):
        return str(self.dimension)

    def set_probability(self, overall_fitness):
        if self.fitness is not None:
            self.probability = self.fitness/overall_fitness

    def get_probability(self):
        return self.probability


def count_occurrence(points_list):
    count_map = {}
    for point in points_list:
        assignment = point.assignment
        if count_map.get(assignment) is not None:
            count_map[assignment] = count_map.get(assignment)+1
        else:
            count_map[assignment] = 1
    return count_map


class State(object):
    def __init__(self, points, chromosomes,
                 clusters, dimensions,
                 mutation, distance_metric):
        """

        :param points: list of point Objects
        :param chromosomes: list of floats that represents the full set of chromosomes i.e the Centroids
        :param clusters: Number of Cluster to Produce
        :param dimensions: Number of Dimension the Points Exist In
        :param mutation: float describing the mutation rate
        :param distance_metric: fn describing the distance metric
        """
        self.points = points
        self.chromosomes = chromosomes
        self.centers = []
        self.mutation_rate = mutation
        self.number_of_clusters = clusters
        self.number_of_dimension = dimensions
        self.distance_metric = distance_metric
        self.overall_fitness = math.inf
        self.count_map = None
        self.re_centered = False
        self.do_assignments()

    def __str__(self):
        return str(self.chromosomes)

    def __repr__(self):
        return str(self.chromosomes)

    def do_assignments(self):
        centers = np.reshape(self.chromosomes,
                             (self.number_of_clusters, self.number_of_dimension))

        label = 1
        for center in centers:
            self.centers.append(Center(center.tolist(), label))
            label += 1

        for point in self.points:
            assignment = [self.distance_metric(point.dimension, center.dimension) for center in self.centers]
            index_min = np.argmin(assignment)
            point.set_assignment(self.centers[index_min].id)

        total_fitness = 0

        for k in range(1, self.number_of_clusters + 1):
            ls = list(filter(lambda x: x.assignment == k, self.points))
            center = centers[k-1]
            relative_fitness = sum(map(lambda x: self.distance_metric(x.dimension, center), ls))
            self.centers[k-1].fitness = relative_fitness
            total_fitness += relative_fitness

        self.overall_fitness = total_fitness

        for center in self.centers:
            center.set_probability(self.overall_fitness)

        self.count_map = count_occurrence(self.points)

    def isvalid(self):
        for k in range(1, self.number_of_clusters+1):
            if self.count_map.get(k) is None or self.count_map.get(k) == 0:
                return False
        return True

    def selection(self, other_state):
        points = copy.deepcopy(self.points)
        centers = copy.deepcopy(self.centers) + copy.deepcopy(other_state.centers)
        centers.sort(key=lambda x: x.get_probability(), reverse=True)
        new_centers = 0
        new_chromosomes = []
        for k in range(len(centers)):
            probability = centers[k].probability
            score = probability * ((1-probability)**k)
            random_v = random.uniform(0, 1)
            if random_v < score and new_centers < self.number_of_clusters:
                new_centers += 1
                p = centers[k].dimension
                new_chromosomes+=p

        if new_centers == self.number_of_clusters:
            return State(points, new_chromosomes,
                         self.number_of_clusters, self.number_of_dimension,
                         self.mutation_rate, self.distance_metric)

        return

    def crossover(self, other_state, k):
        chromosomes1 = copy.deepcopy(self.chromosomes)
        chromosomes2 = copy.deepcopy(other_state.chromosomes)

        crosses = list(random.sample(range(len(chromosomes1)), k))
        crosses.sort()

        new_chromosome_1 = []
        new_chromosome_2 = []

        if 0 not in crosses:
            crosses.insert(0, 0)
        crosses.append(len(chromosomes1))

        # print("Crossover")
        # print("\tK:", k)
        # print("\tCrosses:", crosses)


        # inclusive of first
        # exclusive of second
        for k in range(len(crosses)-1):
            first = crosses[k]
            second = crosses[k+1]
            slice_1 = chromosomes1[first:second]
            slice_2 = chromosomes2[first:second]
            if k % 2 == 0:
                new_chromosome_1 += slice_1
                new_chromosome_2 += slice_2

            else:
                new_chromosome_1 += slice_2
                new_chromosome_2 += slice_1

        new_points_1 = copy.deepcopy(self.points)
        new_points_2 = copy.deepcopy(self.points)

        # print("\tCrossover A:", new_chromosome_1)
        # print("\tCrossover B:", new_chromosome_2)

        return (
            State(new_points_1, new_chromosome_1,
                  self.number_of_clusters, self.number_of_dimension,
                  self.mutation_rate, self.distance_metric),
            State(new_points_2, new_chromosome_2,
                  self.number_of_clusters, self.number_of_dimension,
                  self.mutation_rate, self.distance_metric)
        )

    def mutation(self):
        new_chromosomes_1 = copy.deepcopy(self.chromosomes)
        new_chromosomes_2 = copy.deepcopy(self.chromosomes)

        for k in range(len(new_chromosomes_2)):
            random_v = random.uniform(0, 1)
            if random_v < self.mutation_rate:
                delta = random.uniform(0, 1)
                epsilon = random.uniform(0, 1)

                if random.randint(0, 10) % 2 == 0:
                    new_chromosomes_1[k] = new_chromosomes_1[k] + (delta+epsilon)*new_chromosomes_1[k]
                    new_chromosomes_2[k] = new_chromosomes_2[k] - (delta+epsilon)*new_chromosomes_2[k]
                else:
                    new_chromosomes_1[k] = new_chromosomes_1[k] - (delta + epsilon) * new_chromosomes_1[k]
                    new_chromosomes_2[k] = new_chromosomes_2[k] + (delta + epsilon) * new_chromosomes_2[k]

        new_points_1 = copy.deepcopy(self.points)
        new_points_2 = copy.deepcopy(self.points)

        # print("Mutation")
        # print("\tNew_Chromosomes 1", new_chromosomes_1)
        # print("\tNew_Chromosomes 2", new_chromosomes_2)

        return (
            State(new_points_1, new_chromosomes_1,
                  self.number_of_clusters, self.number_of_dimension,
                  self.mutation_rate, self.distance_metric),
            State(new_points_2, new_chromosomes_2,
                  self.number_of_clusters, self.number_of_dimension,
                  self.mutation_rate, self.distance_metric))

    def re_center(self):
        if not self.re_centered:
            # print("Re-Center")
            # print(self.count_map)
            for k in range(1, self.number_of_clusters + 1):
                ls = list(filter(lambda x: x.assignment == k, self.points))
                # print("\t\tk", len(ls))
                matrix = np.vstack(list(map(lambda x: x.dimension, ls)))
                median = np.median(matrix, axis=0)
                self.centers[k-1].dimension = median.tolist()

            new_chromosomes = []
            for center in self.centers:
                new_chromosomes += center.dimension
            self.chromosomes = new_chromosomes
            # print("\tNew_Chromosomes", new_chromosomes)

        self.re_centered = True


class GeneticAlgorithm(object):
    def __init__(self, per_generation, generations):
        self.NUMBER_OF_GENERATIONS = generations
        self.NUMBER_OF_MINIMUM = per_generation
        self.DISTANCE_MAP = distance_map()
        self.STATE_DICT = []

    def fit(self):
        def make_generation(k):
            print("starting iteration: ", k)
            if k > self.NUMBER_OF_GENERATIONS:
                return

            past_generation = self.STATE_DICT
            next_generation = []

            while len(next_generation) < self.NUMBER_OF_MINIMUM:
                # print("size of next generation:", len(next_generation))
                sampling = random.sample(past_generation, 3)
                state_1 = sampling[0]
                state_2 = sampling[1]
                state_3 = sampling[2]

                new_state_1 = state_1.selection(state_2)

                if new_state_1 is not None and new_state_1.isvalid():
                    next_generation.append(new_state_1)

                new_state_1, new_state_2 = state_2.crossover(state_3, 1)
                if new_state_1.isvalid():
                    next_generation.append(new_state_1)
                if new_state_2.isvalid():
                    next_generation.append(new_state_2)

                new_state_1, new_state_2 = state_3.mutation()
                if new_state_1.isvalid():
                    next_generation.append(new_state_1)
                if new_state_2.isvalid():
                    next_generation.append(new_state_2)

                state_1.re_center()

            self.STATE_DICT = next_generation
            make_generation(k + 1)

        make_generation(1)

    def seed_0(self,gen_0):
        self.STATE_DICT = gen_0

    def get_fittest(self):
        final_states = self.STATE_DICT
        return min(final_states, key=lambda state: state.overall_fitness)








