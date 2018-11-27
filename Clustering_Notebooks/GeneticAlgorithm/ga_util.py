import numpy as np
import random
import math
import copy


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

    def __str__(self):
        return str(self.dimension)

    def set_consistent_id(self, val):
        self.consistent_id = val

    def updated(self):
        if self.consistent_id is not None and self.consistent_id != self.original_id:
            return True
        return False


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
        self.score = math.inf

    def compute_centers(self):
        if len(self.centers) == 0:
            for k in self.number_of_clusters:
                ls = list(filter(lambda x: x.get_assignment() == k+1, self.points))
                matrix = np.vstack(list(map(lambda x: x.dimension, ls)))
                median = np.median(matrix, axis=0)
                self.centers.append(Center(median, k))

    def compute_score(self):
        pass

    def make_consistent(self, other_state):
        if len(self.centers) == 0:
            self.compute_centers()
        if len(other_state.centers) == 0:
            other_state.compute_centers()

        distance_matrix = [[self.distance_metric(i.dimension, j.dimension) for i in other_state.centers]
                           for j in self.centers]

        # TODO: Greedy Assignment
        possible_swaps = [x for x in range(len(distance_matrix))]
        for k in range(len(distance_matrix)):
            dist_row = distance_matrix[k]
            candidate = [distance_matrix[k][x] for x in range(len(distance_matrix)) if x in possible_swaps]
            candidate.sort()
            index_of_other_state = dist_row.index(candidate[0])
            updated_center = [center for center in other_state.centers
                              if center.original_id == index_of_other_state+1][0]
            updated_center.set_consistent_id(k)

        for center in other_state.centers:
            points_assigned = list(filter(lambda x: x.assignment == center.original_id, other_state.points))
            for points in points_assigned:
                points.set_next(center.consistent_id)

        for point in other_state.points:
            point.update()

    def selection(self, other_state):
        self.make_consistent(other_state)
        arr = [0] * len(self.points)
        new_points = copy.deepcopy(self.points)

        for point in new_points:
            point.set_assignment(None)

        candidates = [x for x in range(len(self.points))]
        for k in candidates:
            if self.points[k].assignment == other_state.points[k].assignment:
                new_points[k].assignment = other_state.points[k].assignment
                candidates.remove(k)

    def crossover(self, other_state, k):
        self.make_consistent(other_state)
        crossovers = random.sample(range(len(self.points)), k).sort()

        return

    def mutation(self, k):
        mutation = random.sample(range(len(self.points)), k).sort()
        new_points = copy.deepcopy(self.points)
        count_map = count_occurrence(new_points)
        for x in mutation:
            current = new_points[x]
            if count_map[current.assignment] > 1:
                new_assignment = random.randint(1, self.number_of_clusters)
                count_map[current.assignment] = count_map[current.assignment]-1
                current.assignment = new_assignment
                count_map[current.assignment] = count_map[current.assignment]+1

        return State(new_points, self.number_of_clusters, self.distance_metric)





