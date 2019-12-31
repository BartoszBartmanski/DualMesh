#!/usr/bin/env python

import dualmesh
import meshio
import numpy as np
import unittest

class TestDualmesh(unittest.TestCase):

    def test_array_intersection(self):
        a = [[0, 0], [0, 1]]
        b = [[4, 3], [0, 0], [1, 0]]
        res = dualmesh.array_intersection(a, b)

        self.assertListEqual(res.tolist(), [True, False])

    def test_reorder_points(self):
        points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        new_order = dualmesh.reorder_points(points)

        self.assertListEqual(new_order, [0, 2, 3, 1])

    def test_get_area(self):
        points = np.array([[0, 0], [0.5, 0], [0.5, 1], [0, 1]])
        area = dualmesh.get_area(points)

        self.assertEqual(area, 0.5)

    def test_get_dual_points(self):
        points = np.array([[0, 0], [1.0, 0], [1.0, 1.0], [0, 1]])
        cells = {"vertex": np.array([[0], [1], [2], [3]]),
                 "line": np.array([[0, 1], [1, 2], [2, 3], [3, 0]]),
                 "quad": np.array([[0, 1, 2, 3]])}
        msh = meshio.Mesh(points, cells)

        res = dualmesh.get_dual_points(msh, 0).tolist()
        correct = [[0, 0], [0.5, 0], [0, 0.5], [0.5, 0.5]]
        self.assertListEqual(res, correct)

        res = dualmesh.get_dual_points(msh, 1).tolist()
        correct = [[1, 0], [0.5, 0], [1, 0.5], [0.5, 0.5]]
        self.assertListEqual(res, correct)

        res = dualmesh.get_dual_points(msh, 2).tolist()
        correct = [[1, 1], [1, 0.5], [0.5, 1], [0.5, 0.5]]
        self.assertListEqual(res, correct)

        res = dualmesh.get_dual_points(msh, 3).tolist()
        correct = [[0, 1], [0.5, 1], [0, 0.5], [0.5, 0.5]]
        self.assertListEqual(res, correct)


if __name__ == '__main__':
    unittest.main()
