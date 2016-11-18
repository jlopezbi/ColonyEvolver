import bpy
import sys,os,imp
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)
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
        self.plant = plant.Plant((0.0,0.0,0.0))

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
        np.testing.assert_equal(self.plant.bbox_lower,(0,0,0))
        np.testing.assert_equal(self.plant.bbox_upper,(0,0,0))
        self.plant.append_node(new_node)
        np.testing.assert_equal(self.plant.bbox_upper,(1,1,1))
        new_node = nodes.Node(0,(-1.,10.,1.0))    
        self.plant.append_node(new_node)
        np.testing.assert_equal(self.plant.bbox_lower,(-1.,0.,0.))
        np.testing.assert_equal(self.plant.bbox_upper,(1.,10.,1.))


    def _test_get_new_node_position(self):
        #Test out of date!
        new_node = nodes.Node(0,(1,1,1))    
        self.plant.append_node(new_node)
        p_pos = (2.,2.,0.)
        vec = self.plant._get_new_node_position(p_pos,node_idx=1)
        np.testing.assert_equal(vec,(1.5,1.5,.5))

class NodeTestCase(unittest.TestCase):

    def setUp(self):
        self.plant = plant.Plant((0.0,0.0,0.0))

    def _test_respond_to_collision(self):
        node = nodes.Node(parent = None,coordinates=(0.0,0.0,0.0))

    def test_get_parent_internode_vec(self):
        new_node = nodes.Node(self.plant.nodes[0],(1,2.1,3.4))    
        #self.plant.append_node(new_node)
        #node = self.plant.node[1]
        vec = new_node.get_parent_internode_vec(self.plant)
        np.testing.assert_equal(vec,(1.,2.1,3.4)) 
        
    def test_implements_respond_to_collision(self):
        position = (2.,2.,2.)
        radius = 1.
        node = nodes.Node(parent=self.plant.nodes[0],coordinates=(1.,1.,1.))
        new_node = node.respond_to_collision(self.plant,position,radius)
        node = nodes.SquiggleNode(parent = self.plant.nodes[0],coordinates=(0.0,1.0,1.0))
        node.respond_to_collision(self.plant,position,radius)

        #self.assertIsInstance(new_node,plant.Node)
        #self.plant.show()

    def test_subclasses_add_attributes(self):
        node = nodes.Bud(parent = self.plant.nodes[0], coordinates= (10,10,10))


if __name__=="__main__":
    unittest.main(exit=False)
