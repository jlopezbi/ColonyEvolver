import bpy
import sys,os,imp
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)

import bmesh
import numpy as np
import mesh_helpers as b_help
imp.reload(b_help)

def get_init_object():
    obj = mesh_helpers.init_mesh_object("Box")
    obj.show_bounds = True
    return 

def make_bmesh_extremity_points(lower,upper):
    '''
    make simple mesh with two verts
    and set display to bounding_box
    '''
    bm = bmesh.new()
    bm.verts.new(lower)
    bm.verts.new(upper)
    return bm

def show_bmesh_bounding_box(b_mesh):
    '''
    uses a quick trick to show an axis-aligned box:
    uses show_bounds = True to show bounds of the
    two extremity points in blender
    '''
    me = b_help.write_bmesh_to_mesh(b_mesh)
    name = b_help.add_mesh_to_scene(me)
    bpy.data.objects[name].show_bounds = True

if __name__=="__main__":
    lower = np.array([1.0,1.0,1.0])
    upper = np.array([11,11,5])
    bm = make_bmesh_extremity_points(lower,upper)
    show_bmesh_bounding_box(bm)

