import unittest
import numpy as np
import SimulatedAnnealing as SA


class MyTestCase(unittest.TestCase):
    def test_L1(self):
        a1 = np.array([1,3])
        a2 = np.array([0,0])
        self.assertEqual(SA.L_1(a1, a2), 4)

    def test_L_INF(self):
        a1 = np.array([1, 3])
        a2 = np.array([0, 0])
        self.assertEqual(SA.L_INF(a1, a2), 3)



if __name__ == '__main__':
    unittest.main()
