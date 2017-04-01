import sys,os,imp
import unittest
import numpy as np

import plant
import nodes
imp.reload(plant)
imp.reload(nodes)

class NodeTestCase(unittest.TestCase):

    def setUp(self):
        self.plant = plant.Plant(nodes.Node(parent=None,location=(0,0,0)))

    def _test_respond_to_collision(self):
        node = nodes.Node(parent = None,location=(0.0,0.0,0.0))

    def test_get_parent_internode_vec(self):
        new_node = nodes.Node(self.plant.nodes[0],(1,2.1,3.4))    
        #self.plant.append_node(new_node)
        #node = self.plant.node[1]
        vec = new_node.get_parent_internode_vec(self.plant)
        np.testing.assert_equal(vec,(1.,2.1,3.4)) 
        
    def test_implements_respond_to_collision(self):
        position = (2.,2.,2.)
        radius = 1.
        node = nodes.Node(parent=self.plant.nodes[0],location=(1.,1.,1.))
        new_node = node.respond_to_collision(self.plant,position,radius)
        node = nodes.SquiggleNode(parent = self.plant.nodes[0],location=(0.0,1.0,1.0))
        node.respond_to_collision(self.plant,position,radius)

        #self.assertIsInstance(new_node,plant.Node)
        #self.plant.show()

    def test_subclasses_add_attributes(self):
        node = nodes.Bud(parent = self.plant.nodes[0],location= (10,10,10))

    def test_make_self_child_with_attributes(self):
        class DerivedNode(nodes.Node):
            def _post_initialize(self,kwargs):
                self.a = kwargs['a']
        node = DerivedNode(parent=None,location=[1],a=2)
        new_node = node.make_self_child(location=[1.1],a=2)

if __name__=="__main__":
    unittest.main(verbosity=2)

