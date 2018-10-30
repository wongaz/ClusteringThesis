import unittest
import numpy as np
import SimulatedAnnealing as sa


class MyTestCase(unittest.TestCase):
    def test_L1(self):
        a1 = np.array([1,3])
        a2 = np.array([0,0])
        self.assertEqual(sa.L_1(a1, a2), 4)

    def test_L_INF(self):
        a1 = np.array([1, 3])
        a2 = np.array([0, 0])
        self.assertEqual(sa.L_INF(a1, a2), 3)

    def test_calculate_L1(self):
        pass

    def test_calculate_L_INF(self):
        pass




if __name__ == '__main__':
    unittest.main()