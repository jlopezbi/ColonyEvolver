import unittest,imp
import bpy
import bmesh
import numpy as np
import mesh_helpers
imp.reload(mesh_helpers)

class MeshHelpersTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = mesh_helpers.init_mesh_object() 
        self.bm = mesh_helpers.create_bmesh_from_obj(self.obj)

    def tearDown(self):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all()
        bpy.ops.object.delete()

    def test_add_line_to_bmesh(self):
        mesh_helpers.add_line_to_bmesh(self.bm,(0,0,0),(0,0,1))
        mesh_helpers.show_bmesh(self.bm)

    def test_add_vertices_to_mesh_object(self):
        verts = [(0.0,0.0,0.0),(1.0,1.0,1.0)]
        bm_verts = mesh_helpers.add_vertices_to_mesh_object(self.obj,verts)
        self.assertIsInstance(bm_verts[0],bmesh.types.BMVert)

    def _test_add_edge_to_mesh_object(self):
        verts = [(0.0,0.0,0.0),(1.0,1.0,1.0)]
        v1,v2 = mesh_helpers.add_vertices_to_mesh_object(self.obj,verts)
        print(type(v2))
        print(v2)
        mesh_helpers.add_edge_to_mesh_object(self.obj,v1,v2)

class MeshSkeletonGrowerTestCase(unittest.TestCase):
    def setUp(self):
        self.grower = mesh_helpers.MeshSkeletonGrower()

    def tearDown(self):
        bpy.ops.object.select_all()
        bpy.ops.object.delete()

    def test_add_vertex(self):
        vert = np.array((1.0,0.0,0.0))
        bm_vert = self.grower.add_vertex(vert)
        self.assertIsInstance(bm_vert,bmesh.types.BMVert)

    def test_adds_vertices(self):
        verts = [(0.0,0.0,0.0),(1.0,1.0,1.0)]
        bm_verts = self.grower.add_vertices(verts)
        for bm_vert in bm_verts:
            self.assertIsInstance(bm_vert,bmesh.types.BMVert)

    def test_add_edge(self):
        verts = [(0.0,0.0,0.0),(1.0,1.0,1.0)]
        v1,v2 = self.grower.add_vertices(verts)
        bm_edge = self.grower.add_edge(v1,v2)
        self.assertIsInstance(bm_edge,bmesh.types.BMEdge)


if __name__=="__main__":
    unittest.main(exit=False)
