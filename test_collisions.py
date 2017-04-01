import unittest
import numpy as np
import collisions
import imp
imp.reload(collisions)

m1 =[ [0.0, 0.0, 0.0],
     [0.0,0.0,1.0],
     [0.5,0.5,0.0],
    ]

m2 =[[0.0, 0.0, 3.0],
     [0.0, 0.5, 0.5],
    ]



class dummy_matrixable(object):
    def __init__(self,array):
        self.array = array

    def get_matrix_form(self):
        return np.array(self.array)
dummy1 = dummy_matrixable(m1)
dummy2 = dummy_matrixable(m2)


class CollisionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy1 = dummy_matrixable(m1)
        self.dummy2 = dummy_matrixable(m2)
    def test_create_spatial_tree(self):
        collisions.create_spatial_tree(self.dummy1)
        collisions.create_spatial_tree(self.dummy2)

    def test_collide(self):
        radius = 2.9
        collisions.collide(self.dummy1,self.dummy2, radius)
        

if __name__ == "__main__":
    unittest.main(verbosity=2)


