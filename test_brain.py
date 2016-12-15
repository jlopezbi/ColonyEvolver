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

    def test_make_vec_pset(self):
        pset = brain.make_vec_pset()

