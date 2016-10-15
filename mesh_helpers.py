import bpy
import bmesh
import unittest
#NOTE: for some reason all geometry added to the
#blender document is parented at the moment
def init_mesh_object(name="Object"):
    me = bpy.data.meshes.new("Mesh")
    scene = bpy.context.scene
    obj = bpy.data.objects.new(name, me)
    scene.objects.link(obj)
    return obj

def init_bmesh():
    return bmesh.new()

def prep_mesh_object(obj):
    ''' sets object active and in edit mode, and retrieves the mesh
    '''
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    me =  obj.data
    return me

def object_mode():
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def add_line_to_mesh_object(obj,start,end):
    me = prep_mesh_object(obj)
    add_line_to_mesh(me,start,end)
    object_mode()

def add_vertices_to_mesh_object(obj,verts):
    me = prep_mesh_object(obj)
    bm = bmesh.from_edit_mesh(me)
    for vert in verts:
        bm.verts.new(vert)
    bmesh.update_edit_mesh(me)
    object_mode()

def add_line_to_mesh(mesh,start,end):
    bm = bmesh.from_edit_mesh(mesh)
    add_line_to_bmesh(bm,start,end)
    bmesh.update_edit_mesh(mesh)

def add_line_to_bmesh(bmesh,start,end):
    v_start = bmesh.verts.new(start)
    v_end = bmesh.verts.new(end)
    bmesh.edges.new((v_start,v_end))

def show_bmesh(bmesh):
    mesh = write_bmesh_to_mesh(bmesh)
    return add_mesh_to_scene(mesh)

def write_bmesh_to_mesh(bmesh):
    new_mesh = bpy.data.meshes.new("Mesh")
    bmesh.to_mesh(new_mesh)
    return new_mesh

def add_mesh_to_scene(mesh,object_name="Object"):
    scene = bpy.context.scene
    obj = bpy.data.objects.new(object_name, mesh)
    scene.objects.link(obj)
    return object_name

class MeshHelpersTestCase(unittest.TestCase):
        
    def setUp(self):
        self.obj = init_mesh_object()
        self.bm = bmesh.new()

    def test_add_line_to_bmesh(self):
        add_line_to_bmesh(self.bm,(0,0,0),(0,0,1))
        show_bmesh(self.bm)

    def test_add_line_to_mesh(self):
        a = (0,0,0)
        b = (0,1,1)
        c = (1,1,1)
        add_line_to_mesh_object(self.obj,a,b)
        add_line_to_mesh_object(self.obj,b,c)

    def test_add_vertices_to_mesh_object(self):
        verts = ((1,1,0),(2,2,0))
        add_vertices_to_mesh_object(self.obj,verts)

if __name__=="__main__":
    unittest.main(exit=False)
