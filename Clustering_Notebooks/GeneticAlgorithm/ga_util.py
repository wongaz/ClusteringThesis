import numpy as np
import random
import math


class Point(object):
    def __init__(self, dimension, assignment):
        self.dimension = dimension
        self.assignment = assignment
        self.next = None

    def __str__(self):
        return str(self.assignment)

    def set_assignment(self, val):
        self.assignment = val

    def set_next(self, val):
        if val != self.assignment:
            self.next = val
            return True
        return False

    def reset(self):
        self.next = None

    def update(self):
        if self.next is not None:
            self.assignment = self.next
        self.next = None

    def get_assignment(self):
        if self.next is None:
            return self.assignment
        return self.next


class Center(object):
    def __init__(self, dimension, label):
        self.dimension = dimension
        self.original_id = label
        self.consistent_id = None

    def set_consistent_id(self, val):
        self.consistent_id = val

    def updated(self):
        if self.consistent_id is not None and self.consistent_id != self.original_id:
            return True
        return False


class State(object):
    def __init__(self, points, distance_metric):
        '''

        :param points:
        :param distance_metric:
        '''
        self.points = points
        self.centers = []
        self.distance_metric = distance_metric
        self.score = math.inf

    def compute_centers(self):
        if len(self.centers) == 0:
            cluster_id = {point.get_assignment() for point in self.points}
            for k in cluster_id:
                ls = list(filter(lambda x: x.get_assignment() == k, self.points))
                matrix = np.vstack(list(map(lambda x: x.dimension, ls)))
                median = np.median(matrix, axis=0)
                self.centers.append(Center(median, k))

    def make_consistent(self, other_state):
        if len(self.centers) == 0:
            self.compute_centers()
        if len(other_state.centers) == 0:
            other_state.compute_centers()

        distance_matrix = [[self.distance_metric(i.dimension, j.dimension) for i in other_state.centers]
                           for j in self.centers]

        possible_swaps = [x for x in range(len(distance_matrix))]
        for k in range(len(distance_matrix)):
            original_dist = distance_matrix[k]
            candidate = [distance_matrix[k][x] for x in len(distance_matrix) if x in possible_swaps]
            candidate.sort()
            index = original_dist.index(candidate[0])
            if index in possible_swaps:
                possible_swaps.remove(index)

    def selection(self, other_state):
        self.make_consistent(other_state)

    def crossover(self, other_state, k):
        self.make_consistent(other_state)
        return

    def mutation(self, k):
        return





