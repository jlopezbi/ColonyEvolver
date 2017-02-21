import imp
import numpy as np
import mathutils
import unittest
import vector_operations
imp.reload(vector_operations)

class VectorOperationsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_ortho(self):
        vec = mathutils.Vector((1.0,55.0,0.0))
        o = vector_operations.get_ortho(vec)
        self.assertEqual(o.dot(vec), 0)
        self.assertAlmostEqual(o.length,vec.length,places=5)

        vec = (0.0,0.0,0.0)
        o = vector_operations.get_ortho(vec)
        self.assertEqual(o.dot(vec), 0)

    def test_make_star_burst(self):
        vec = (1.0,0.0,0.0)
        axis = (0.0,0.0,1.0)
        num = 4
        burst = vector_operations.make_star_burst(vec,axis,num)
        self.assertTrue(len(burst)==num)
        np.testing.assert_almost_equal(burst[1],(0.0,1.0,0.0))


if __name__=="__main__":
    unittest.main(verbosity=2)

