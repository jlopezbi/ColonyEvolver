import sys,os,imp
import unittest
import numpy as np
import mathutils

import plant
import nodes
imp.reload(plant)
imp.reload(nodes)

class StubbedParticleSystem(object):
    def __init__(self,n_particles=10):
        self.n_particles = n_particles
        self.particles = [StubbedParticle() for i in range(self.n_particles)]

class StubbedParticle(object):
    def __init__(self,location=(0.0,0.0,0.0),radius=2.0):
        self.position = np.array(location)
        self.radius = radius

class PlantTestCase(unittest.TestCase):
    def setUp(self):
        self.plant = plant.Plant(nodes.DumbNode(parent=None,location=(0.0,0.0,0.0)))

    def test_show(self):
        self.plant.show()
        new_node = nodes.Node(self.plant.nodes[0],(1,1,1))
        self.plant.append_node(new_node)
        self.plant.show()

    def test_translate(self):
        new_node = nodes.Node(self.plant.nodes[0],(1,1,0))
        self.plant.append_node(new_node)
        self.plant.show()
        self.plant.translate((1,1,1))


    def test_updates_bbox_when_node_added(self):
        new_node = nodes.Node(0,(1,1,1))    
        np.testing.assert_equal(self.plant.bbox.bbox_lower,(0,0,0))
        np.testing.assert_equal(self.plant.bbox.bbox_upper,(0,0,0))
        self.plant.append_node(new_node)
        np.testing.assert_equal(self.plant.bbox.bbox_upper,(1,1,1))
        new_node = nodes.Node(0,(-1.,10.,1.0))    
        self.plant.append_node(new_node)
        np.testing.assert_equal(self.plant.bbox.bbox_lower,(-1.,0.,0.))
        np.testing.assert_equal(self.plant.bbox.bbox_upper,(1.,10.,1.))


    def _test_get_new_node_position(self):
        #Test out of date!
        new_node = nodes.Node(0,(1,1,1))    
        self.plant.append_node(new_node)
        p_pos = (2.,2.,0.)
        vec = self.plant._get_new_node_position(p_pos,node_idx=1)
        np.testing.assert_equal(vec,(1.5,1.5,.5))

if __name__=="__main__":
    unittest.main(verbosity=2)
