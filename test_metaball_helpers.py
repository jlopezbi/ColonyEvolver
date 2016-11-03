import unittest

import numpy as np
import sys,os,imp
import bpy
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)

import metaball_helpers as mhelp
imp.reload(mhelp)

class MetaballHelpersTestCase(unittest.TestCase):

    def setUp(self):
        obj,mball = mhelp.create_metaball_obj()
        self.obj = obj
        self.mball = mball

    def _test_create_metball_obj(self):
        bpy.context.scene.objects.link(self.obj)

    def _test_add_metaball_sphere(self):
        pos = np.array((1.,1.,1.))
        radius = 1.0
        self.mball.elements.new() #default is sphere

    def test_add_metaball_rod(self):
        start = np.array((0.,0.,0.))
        end = np.array((10.,10.,0.))
        radius = 1.0
        ele = mhelp.add_metaball_rod(self.mball,radius,start,end)
        np.testing.assert_equal(np.array(ele.co),(5.,5.,0.0))
        self.assertAlmostEqual(ele.size_x*2.0,14.142,places=3)





if __name__ == "__main__":
    unittest.main(exit=False)
