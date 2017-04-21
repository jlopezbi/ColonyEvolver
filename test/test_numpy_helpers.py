import unittest
import numpy_helpers
import numpy as np

class VectorHelperFunctionsTestCase(unittest.TestCase):

    def test_get_mean_vector(self):
        v1 = (1.0,0.0,0.0)
        v2 = (0.0,1.0,0.0)
        actual = numpy_helpers.get_mean_vector([v1,v2])
        actual = numpy_helpers.get_mean_vector((v1,v2))
        desired = ( .5,  .5, 0.0)
        np.testing.assert_almost_equal(actual,desired,decimal=7)

    def test_get_weighted_average_vectors(self):
        v1 = (1.0,0.0,0.0)
        v2 = (0.0,1.0,0.0)
        weights = (.7,.3)
        actual = numpy_helpers.get_weighted_average_vectors((v1,v2),weights)
        desired = ( .7,  .3, 0.0)
        np.testing.assert_almost_equal(actual,desired,decimal=7)

        

