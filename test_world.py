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

    def test_resize_to_fit(self):
        bbox_lower = np.array((-1.,-3.,0.))
        bbox_upper = np.array((12.,4.,4.))
        self.box.resize_to_fit(bbox_lower,bbox_upper,1.)
        np.testing.assert_equal(self.box.lower_vertex,(-2.0,-4.0,0.))
        np.testing.assert_equal(self.box.upper_vertex,(13.,5.,5.))

    def test_show(self):
        self.box.show()

    def test_translate(self):
        self.box.translate((1,1,1))
        self.box.show()
        #TODO: actually test coordinates


if __name__=="__main__":
    unittest.main(exit=False)
        
