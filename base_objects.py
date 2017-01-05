import imp
import numpy as np
import math,random

import numpy_helpers
imp.reload(numpy_helpers)


class BoundingBox(object):

    def __init__(self,lower=(0.,0.,0.),upper=(0.,0.,0.)):
        greater_or_equal = np.greater(upper,lower).all() or np.equal(upper,lower).all()
        assert greater_or_equal, 'front vertex {} must be greater than back_vertex {}'.format(front_vertex,back_vertex)
        self.bbox_lower = np.array(lower)
        self.bbox_upper = np.array(upper)

    def update_bbox(self,test_location):
        self.bbox_lower = np.minimum(self.bbox_lower,test_location)
        self.bbox_upper = np.maximum(self.bbox_upper,test_location)

    def calculate_volume(self):
        return self.dimension_along(0) * self.dimension_along(1) * self.dimension_along(2)

    def dimension_along(self,axis):
        '''
        axis = (0, 1, 2) representing (x, y, z)
        '''
        l,u = self._range_along(axis)
        return u-l

    def _range_along(self,axis):
        assert axis in (0,1,2), 'axis was {}, must be one of 0 (x) 1 (y) or 2 (z)'.format(axis)
        return self.bbox_lower[axis], self.bbox_upper[axis]
