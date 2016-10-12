import unittest,imp
import mesh_helpers
imp.reload(mesh_helpers)

class MeshHelpersTestCase(unittest.TestCase):
    def setUp(self):
        self.bm = mesh_helpers.init_bmesh()
    def test_add_line_to_bmesh(self):
        mesh_helpers.add_line_to_bmesh(self.bm,(0,0,0),(0,0,1))
        mesh_helpers.show_bmesh(self.bm)

if __name__=="__main__":
    unittest.main(exit=False)
