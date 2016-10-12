import bpy
import bmesh

def init_bmesh():
    return bmesh.new()

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
