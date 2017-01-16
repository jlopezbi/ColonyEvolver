import bpy
import sys,os,imp
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)
import unittest
import numpy as np
import mathutils
import brain
imp.reload(brain)

class BrainTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def _make_tree(self,pset):
        return brain.generate_processor_tree(pset,1,4)

    def test_make_vec_pset(self):
        self.pset = brain.make_vec_pset()
        tree,func = self._make_tree(self.pset)

    def test_big_pset(self):
        self.pset = brain.big_pset()
        tree,func = self._make_tree(self.pset)

    def test_save_processor_tree(self):
        self.pset = brain.big_pset()
        tree,func = self._make_tree(self.pset)
        brain.save_processor_tree(tree)

    def test_load_text(self):
        self.test_save_processor_tree()
        tree_text = brain.load_text("tree.txt")
        self.assertIsInstance(tree_text,str)

    def test_resurrect_processor_tree(self):
        self.test_save_processor_tree()
        tree,func = brain.resurrect_processor_tree(self.pset)
        self.assertIsInstance(func,type(lambda x:1))

    def test_plot_genealogy_tree(self):
        tree = {1: (), 2: (), 3: (), 4: (1, 3), 5: (4, 3), 6: (4, 3)}
        brain.plot_genealogy_tree(tree)








