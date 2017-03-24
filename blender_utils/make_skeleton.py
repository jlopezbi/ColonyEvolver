import bpy
import bmesh
import numpy as np
from collections import namedtuple  

def load(file_name='line_data.npy'):
    data = np.load(file_name,encoding='bytes')
    #data is an np array with dimension zero (one element)
    return data[()]

def convert_data(data):
    x = data[b'x']
    y = data[b'y']
    z = data[b'z']
    connections = data[b'connections']
    return x, y, z, connections

def get_full_path(file_name):
    pass

def make_mesh_skeleton(x,y,z,connections):
    grower = MeshSkeletonGrower()
    for i,a in enumerate(x):
        vert = ( x[i], y[i], z[i] )
        v = grower.add_vertex(vert)
    grower.bm.verts.ensure_lookup_table()
    for connection in connections:
        idx1 = connection[0]
        idx2 = connection[1]    
        if idx1 != idx2:
            v1 = grower.bm.verts[idx1]
            v2 = grower.bm.verts[idx2]
            grower.add_edge(v1,v2)
    grower.finalize()

class MeshSkeletonGrower(object):
    '''
    example use case:
    grower = MeshSkeletonGrower()
    v1 = grower.add_vertices((0.0,0.0,0.0))
    #do some stuff
    v2 = grower.add_vertices((10.0,0.0,3.0))
    grower.add_edge((v1,v2))
    #at the very end:
    grower.finalize()
    '''
    def __init__(self,obj_name='Object',mesh_name='mesh'):
        self.obj_name = obj_name
        self.mesh_name = mesh_name
        self.me = bpy.data.meshes.new(self.mesh_name)
        self.bm = bmesh.new()

    def _prepare_to_add_geom(self):
        return bmesh.from_edit_mesh(self.me)
    
    def add_vertex(self,location):
        return self.bm.verts.new(location)

    def add_vertices(self,vertices):
        bm_verts = []
        for vert in vertices:
            new_vert = self.bm.verts.new(vert)
            bm_verts.append(new_vert)
        return bm_verts
    
    def add_edge(self,v1,v2):
        return self.bm.edges.new((v1,v2))

    def finalize(self):
        self.bm.to_mesh(self.me)
        self.bm.free()
        scene = bpy.context.scene
        self.obj = bpy.data.objects.new(self.obj_name, self.me)
        scene.objects.link(self.obj)
        return self.obj

