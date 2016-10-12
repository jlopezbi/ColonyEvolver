import unittest,imp
import world
import numpy as np
imp.reload(world)

class BoxWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.low = np.array([0.0,0.0,0.0])
        self.high = np.array([10.0,10.0,10.0])
        self.box = world.BoxWorld(self.low,self.high)

    def test_in_box_bounds(self):
        pos_vec = np.array([5,5,5])
        result = self.box.in_box_bounds(pos_vec)
        self.assertTrue(result)
        post_vec_on_edge = np.array([10.0,10.0,10.0])
        self.assertFalse(self.box.in_box_bounds(post_vec_on_edge))
        pos_vec_out = np.array([0.0,11.0,5.0])
        self.assertFalse(self.box.in_box_bounds(pos_vec_out))


if __name__=="__main__":
    unittest.main(exit=False)
        
