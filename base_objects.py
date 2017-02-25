import imp
import numpy as np
import math,random

import numpy_helpers
import visualization_base
imp.reload(numpy_helpers)
imp.reload(visualization_base)


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

    def box_seq(self):
        points = np.array(self.collect_points())
        i = [0,1,2,3,0,4,5,1,5,6,2,6,7,3,7,4]
        seq = points[i]
        return seq

    def show(self,ax=None):
        imp.reload(visualization_base)
        ax = visualization_base.init_fig()
        visualization_base.draw_box(self.collect_points(),ax)
        visualization_base.show()
        
    def collect_points(self):
        v1 = self.bbox_lower
        v2 = (self.bbox_upper[0],self.bbox_lower[1],self.bbox_lower[2])
        v3 = (self.bbox_upper[0],self.bbox_upper[1],self.bbox_lower[2])
        v4 = (self.bbox_lower[0],self.bbox_upper[1],self.bbox_lower[2])
        v5 = (self.bbox_lower[0],self.bbox_lower[1],self.bbox_upper[2])
        v6 = (self.bbox_upper[0],self.bbox_lower[1],self.bbox_upper[2])
        v7 = self.bbox_upper
        v8 = (self.bbox_lower[0],self.bbox_upper[1],self.bbox_upper[2])
        return [v1, v2, v3, v4, v5, v6, v7, v8 ]

