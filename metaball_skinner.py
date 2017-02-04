import bpy
import imp
import mesh_helpers
import metaball_helpers
imp.reload(mesh_helpers)
imp.reload(metaball_helpers)

class MetaballSkinner(object):

    def __init__(self, mesh, mball=None, resolution=.06, radius = .08):
        self.mesh = mesh
        if mball==None:
            obj,mball = metaball_helpers.create_metaball_obj(obj_name='MetaSkinned',metaball_name='MBall')
        self.mball = mball
        self.resolution = resolution
        self.radius = radius

    def metaball_rod_maker(self,start,end):
        metaball_helpers.add_metaball_rod(self.mball, self.radius, start, end)

    def skin_mesh(self):
        mesh_helpers.map_to_each_edge_coordinates(self.metaball_rod_maker, self.mesh)


def skin_mesh(mesh, resolution=.06, radius=.08):
    '''Function that creates 'wire-frame' of metaball rods coincident with mesh edges'''
    obj,mball = metaball_helpers.create_metaball_obj(obj_name='MetaSkinned',metaball_name='MBall')

    def metaball_rod_maker(start,end):
        metaball_helpers.add_metaball_rod(mball, radius, start, end)

    mesh_helpers.map_to_each_edge_coordinates(metaball_rod_maker, mesh)

