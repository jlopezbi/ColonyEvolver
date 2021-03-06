import bpy
import bmesh
import numpy as np
import os

def directory_to_skeletons(directory):
    '''
    To Use: Drag and drop folder containing the line data (as .npy files) to get the input 'directory' string.
    MUST CONTAIN ONLY .npy files
    - makes all skeletons in same place
    - watch out for .DS_store
    '''
    file_names = os.listdir(directory)
    for item in file_names:
        path = os.path.join(directory, item)
        obj = file_to_skeleton(path)



def file_to_skeleton(file_name):
    '''TIP: drag and drop file from finder into blender console to get file_name
    Makes blender mesh skeleton from data in file
    note: this only works when the file is a .npy 
    and was saved as an array of a dict. The dict contains 
    the x, y, z, and connections fields'''
    raw = load(file_name)
    x,y,z,c = convert_data(raw)
    obj = make_mesh_skeleton(x,y,z,c)
    return obj
    #obj.location = b

def get_full_path(file_name):
    pass

def get_file_names(directory):
    return os.listdir(directory)


def load(file_name='line_data.npy'):
    data = np.load(file_name,encoding='bytes')
    #data is an np array with dimension zero (one element)
    return data[()]

def convert_data(data):
    '''
    data is loaded in as byte stream, so I guess that is 
    why keys are 'b'
    '''
    x = data[b'x']
    y = data[b'y']
    z = data[b'z']
    connections = data[b'connections']
    return x, y, z, connections

def make_mesh_skeleton(x,y,z,connections):
    grower = MeshSkeletonGrower(obj_name='Skeleton',mesh_name='SkeletonMesh')
    for u,v,w in zip(x,y,z):
        vert = ( u, v, w )
        grower.add_vertex(vert)
    grower.prep_for_edge_adding()
    for connection in connections:
        idx1 = connection[0]
        idx2 = connection[1]    
        if idx1 != idx2:
            v1 = grower.bm.verts[idx1]
            v2 = grower.bm.verts[idx2]
            grower.add_edge(v1,v2)
    return grower.finalize()

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

    def add_vertex(self,location):
        return self.bm.verts.new(location)

    def add_vertices(self,vertices):
        bm_verts = []
        for vert in vertices:
            new_vert = self.bm.verts.new(vert)
            bm_verts.append(new_vert)
        return bm_verts

    def prep_for_edge_adding(self):
        self.bm.verts.ensure_lookup_table()

    def add_edge(self,v1,v2):
        return self.bm.edges.new((v1,v2))

    def finalize(self):
        self.bm.to_mesh(self.me)
        self.bm.free()
        scene = bpy.context.scene
        self.obj = bpy.data.objects.new(self.obj_name, self.me)
        scene.objects.link(self.obj)
        return self.obj

if __name__=="__main__":
    pass


