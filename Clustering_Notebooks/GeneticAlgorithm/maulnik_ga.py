import numpy as np
import random
import math
import copy


class Point(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.assignment = None

    def __str__(self):
        return str(self.assignment)

    def set_assignment(self, val):
        self.assignment = val


class Center(object):
    def __init__(self, dimension, label):
        self.dimension = dimension
        self.id = label
        self.fitness = None

    def __str__(self):
        return str(self.dimension)


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
    def __init__(self, points, clusters, distance_metric):
        '''

        :param points:
        :param distance_metric:
        '''
        self.points = points
        self.centers = []
        self.number_of_clusters = clusters
        self.distance_metric = distance_metric
        self.overall_fitness = math.inf

    def do_assignments(self):
        for point in self.points:
            assignment = [self.distance_metric(point.dimension, center.dimension) for center in self.centers]
            index_min = np.min(assignment)
            point.set_assignment(self.centers[index_min].id)

        total_fitness = 0

        for k in range(1, self.number_of_clusters + 1):
            ls = list(filter(lambda x: x.get_ass == k, self.points))
            center = self.centers[k-1].dimension
            relative_fitness = sum(map(lambda x: self.distance_metric(x.dimension, center), ls))
            self.centers[k-1].fitness = relative_fitness
            total_fitness += relative_fitness

        self.overall_fitness = total_fitness



