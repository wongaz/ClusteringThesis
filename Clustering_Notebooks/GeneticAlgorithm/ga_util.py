import random
from collections import Counter


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


class State(object):
    def __init__(self, points):
        '''
        Constructor for initializing the state
        :param points: A collection of Points
        '''
        self.points = points

    def crossover(self, other_state):

        return

    def mutation(self):
        pass

    def selection(self):
        pass



