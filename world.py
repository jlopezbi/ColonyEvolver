import numpy as np
import math,random
import bpy
import sys,os,imp
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)
import mesh_helpers
imp.reload(mesh_helpers)

class BoxWorld(object):
    """ world defines bounds for nutrients and creature """
    #This should be a very stable class in the project
    #might be neat to avoid depending on blender stuff much; blender is really just for visualization!


    def __init__(self,front_vertex,back_vertex):
        self.lower_vertex = np.array(front_vertex)
        self.upper_vertex = np.array(back_vertex)
        self.padding = 1.0
        self.offset= .001
        self.blender_object = mesh_helpers.init_mesh_object("BoxWorld") 
        self.blender_object.show_bounds = True

    def set_size(self,front,back):
        self.lower_vertex = front
        self.upper_vertex = back

    def show(self):
        mesh_helpers.add_vertices_to_mesh_object(self.blender_object,[self.lower_vertex,self.upper_vertex])

    def translate(self,vector):
        '''
        move the visualization belner object of boxworld
        does not update the true boxworld coordinates
        '''
        self.blender_object.location = vector

    def get_a_spawn_location(self):
        return self._get_random_pos_on_top()

    def _get_random_pos_on_top(self):
        '''
        returns x,y,z coordinates for a random point on the top
        face of this BoxWorld. Note that the x,y position could lie
        on the edge of the top-face
        '''
        x_lower,x_upper = self._shrink_range_by_padding(self._x_range())
        y_lower,y_upper = self._shrink_range_by_padding(self._y_range())
        z = self._top_position() - self.offset
        x = random.uniform(x_lower,x_upper)
        y = random.uniform(y_lower,y_upper)
        return x,y,z
    
    def _shrink_range_by_padding(self,domain):
        upper,lower = domain
        return upper-self.offset, lower+self.offset

    def _x_range(self):
        return self.upper_vertex[0],self.lower_vertex[0]

    def _y_range(self):
        return self.lower_vertex[1],self.upper_vertex[1]

    def _top_position(self):
        return self.upper_vertex[2]
    
    def front_left(self):
        copy = np.copy(self.lower_vertex)
        np.put(copy,0,self.upper_vertex[0])
        return copy
    
    def x_dimension(self):
        return self.upper_vertex[0] - self.lower_vertex[0]

    def particle_is_inside(self,particle):
        '''
        return true if particle is inside world, not including boundary
        return false otherwise
        
        '''
        return self.in_box_bounds(particle.position)

    def in_box_bounds(self,test_vec):
        '''
        return true if test_vec (position) is inside
        the rectangular box defined by lower and upper vertex
        note if the tes_vec lies exaclty on the box boundary this returns False
        '''
        above_min = np.greater(test_vec,self.lower_vertex).all()
        below_max = np.greater(self.upper_vertex,test_vec).all()
        return above_min and below_max

    def resize_to_fit(self,bbox_lower,bbox_upper,padding=None):
        '''
        resize world so that it offsets the box defined by
        bbox_lower and _upper by padding amount
        In all directions except negative z
        '''
        if not padding:
            padding = self.padding
        lower_offset = np.array((padding,padding,0.))
        self.lower_vertex = bbox_lower - lower_offset
        upper_offset = np.array([padding]*3)
        self.upper_vertex = bbox_upper + upper_offset





