import bpy
import sys,os,imp
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)
import unittest
import numpy as np
import mathutils

import plant
imp.reload(plant)

class StubbedParticle(object):
    def __init__(self,location=(0.0,0.0,0.0),radius=2.0):
        self.position = np.array(location)
        self.radius = radius

class PlantTestCase(unittest.TestCase):
    def setUp(self):
        self.plant = plant.Plant((0.0,0.0,0.0))

    def test_show(self):
        self.plant.show()

    def test_grow_collided(self):
        N = 2
        particles = [StubbedParticle() for i in range(N)]
        particles = [StubbedParticle((0,0,1),3)]
        self.plant.grow_collided(particles)
        self.assertTrue(self.plant.number_of_elements(),2)
        self.plant.show()

    def test_updates_bbox_when_node_added(self):
        new_node = plant.Node(0,(1,1,1))    
        np.testing.assert_equal(self.plant.bbox_lower,(0,0,0))
        np.testing.assert_equal(self.plant.bbox_upper,(0,0,0))
        self.plant._add_node(new_node)
        np.testing.assert_equal(self.plant.bbox_upper,(1,1,1))
        new_node = plant.Node(0,(-1.,10.,1.0))    
        self.plant._add_node(new_node)
        np.testing.assert_equal(self.plant.bbox_lower,(-1.,0.,0.))
        np.testing.assert_equal(self.plant.bbox_upper,(1.,10.,1.))

    def test_get_parent_internode_vec(self):
        new_node = plant.Node(0,(1,1,1))    
        self.plant._add_node(new_node)
        vec = self.plant.get_parent_internode_vec(1)
        np.testing.assert_equal(vec,(1.,1.,1.)) 

    def _test_get_new_node_position(self):
        #Test out of date!
        new_node = plant.Node(0,(1,1,1))    
        self.plant._add_node(new_node)
        p_pos = (2.,2.,0.)
        vec = self.plant._get_new_node_position(p_pos,node_idx=1)
        np.testing.assert_equal(vec,(1.5,1.5,.5))
        
if __name__=="__main__":
    unittest.main(exit=False)
