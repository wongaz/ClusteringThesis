import unittest
import math
import numpy as np
import SimulatedAnnealing as sa
from Point import *


class DistanceCalculations(unittest.TestCase):
    def setUp(self):
        self.a1 = np.array([1, 3])
        a1_point = Point(1, self.a1, 1)
        self.a2 = np.array([0, 0])
        a2_point = Point(2, self.a2, 1)
        self.a_list = [a1_point, a2_point]

        self.b1 = np.array([7, 4])
        b1_point = Point(3, self.b1, 2)
        self.b2 = np.array([2, 5])
        b2_point = Point(4, self.b2, 2)
        self.b3 = np.array([3, 8])
        b3_point = Point(5, self.b3, 2)

        self.b_list = [b1_point, b2_point, b3_point]
        self.both_list = self.a_list+self.b_list

    def test_L1(self):
        self.assertEqual(sa.l_1(self.a1, self.a2), 4)

    def test_L_INF(self):
        self.assertEqual(sa.l_infty(self.a1, self.a2), 3)

    def test_L_2(self):
        self.assertEqual(sa.l_2(self.a1, self.a2), math.sqrt(10))

    def test_calculate_L1_1(self):
        sa.DISTANCE = sa.l_1
        self.assertEqual(sa.calculate_score(self.a_list, 1), 4)
        self.assertEqual(sa.calculate_score(self.b_list, 2), 9)
        self.assertEqual(sa.calculate_score(self.both_list, 2), 13)

    def test_calculate_L_INF(self):
        sa.DISTANCE = sa.l_infty
        self.assertEqual(sa.calculate_score(self.a_list, 1), 3)
        self.assertEqual(sa.calculate_score(self.b_list, 2), 8)
        self.assertEqual(sa.calculate_score(self.both_list, 2), 11)

    def test_calculate_L_2(self):
        sa.DISTANCE = sa.l_2
        self.assertEqual(sa.calculate_score(self.a_list, 1), 3.1622776601683795)
        self.assertEqual(sa.calculate_score(self.b_list, 2), 8.123105625617661)
        self.assertEqual(sa.calculate_score(self.both_list, 2), 11.285383285786041)


if __name__ == '__main__':
    unittest.main()