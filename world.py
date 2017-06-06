import numpy as np
import math,random
#import mesh_helpers

#NOTE: both world and plant make use of a bounding box object with the same requirements.
#this object exists and is being used by plant, but further work is required to make it used by boxworld

class BoxWorld(object):
    """ world defines bounds for nutrients and creature """
    #This should be a very stable class in the project
    #might be neat to avoid depending on blender stuff much; blender is really just for visualization!


    def __init__(self,front_vertex,back_vertex):
        '''
        front_vertex and back_vertex are stricly the negative most corner and
        the positive most corner. This assumption is critical for most boxWorld 
        operations.
        '''
        self.lower_vertex = np.array(front_vertex)
        self.upper_vertex = np.array(back_vertex)
        greater_or_equal = np.greater(self.upper_vertex,self.lower_vertex).all() or np.equal(self.upper_vertex,self.lower_vertex).all()
        assert greater_or_equal, 'front vertex {} must be greater than back_vertex {}'.format(front_vertex,back_vertex)
        self.padding = 1.0
        self.padding_multiplier = 2.0
        self.offset= .001
        self.blender_object = None
        self.obj_name = 'BoxWorld'
        self.mesh_name = 'boxMesh'
        #self.mesh_grower = self.setup_mesh_grower()

    def set_size(self,front,back):
        self.lower_vertex = front
        self.upper_vertex = back

    def setup_mesh_grower(self):
        #return mesh_helpers.MeshSkeletonGrower(self.obj_name,self.mesh_name)
        pass

    def report(self):
        '''return a string of relevant information about current state of box'''
        bbox = 'verts: ' + str(self.lower_vertex) + ' ' + str(self.upper_vertex)
        dimensions = 'dimensions: ' + ','.join((str(self.dimension_along(0)),str(self.dimension_along(1)), str(self.dimension_along(2))))
        string =  bbox + '\n' + dimensions
        return bbox

    def show(self):
        '''
        create a mesh composed of edges of this box
        vertex specification starts at lower corner and goes CW around bottom square,
        then cw around top square, adding edges as it goes
        '''
        # if a blender object already exists then the mesh_grower must have been finalized;
        # in this case make a new mesh_grower and object
        '''
        if self.blender_object:
            self.mesh_grower = self.setup_mesh_grower()
        v1 = self.mesh_grower.add_vertex(self.lower_vertex)
        v2 = self.mesh_grower.add_vertex((self.lower_vertex[0],self.upper_vertex[1],self.lower_vertex[2]))
        self.mesh_grower.add_edge(v1,v2)
        v3 = self.mesh_grower.add_vertex((self.upper_vertex[0],self.upper_vertex[1],self.lower_vertex[2]))
        self.mesh_grower.add_edge(v2,v3)
        v4 = self.mesh_grower.add_vertex((self.upper_vertex[0],self.lower_vertex[1],self.lower_vertex[2]))
        self.mesh_grower.add_edge(v3,v4)
        self.mesh_grower.add_edge(v4,v1)
        v5 = self.mesh_grower.add_vertex((self.lower_vertex[0],self.lower_vertex[1],self.upper_vertex[2]))
        self.mesh_grower.add_edge(v1,v5)
        v6 = self.mesh_grower.add_vertex((self.lower_vertex[0],self.upper_vertex[1],self.upper_vertex[2]))
        self.mesh_grower.add_edge(v2,v6)
        self.mesh_grower.add_edge(v5,v6)
        v7 = self.mesh_grower.add_vertex(self.upper_vertex)
        self.mesh_grower.add_edge(v3,v7)
        self.mesh_grower.add_edge(v6,v7)
        v8 = self.mesh_grower.add_vertex((self.upper_vertex[0],self.lower_vertex[1],self.upper_vertex[2]))
        self.mesh_grower.add_edge(v4,v8)
        self.mesh_grower.add_edge(v7,v8)
        self.mesh_grower.add_edge(v8,v5)
        self.blender_object = self.mesh_grower.finalize()
        '''
        #print("show for box world not implemented yet!")
        pass

    def translate(self,vector):
        '''
        move the visualization belner object of boxworld
        does not update the true boxworld coordinates
        '''
        if self.blender_object: self.blender_object.location = vector

    def get_a_spawn_location(self):
        #func = random.choice((self._get_random_pos_on_top,self._get_random_pos_on_back))
        func = self._get_random_pos_on_top
        return func()

    def _get_random_pos_on_top(self):
        '''
        returns x,y,z coordinates for a random point on the top
        face of this BoxWorld. Note that the x,y position could lie
        on the edge of the top-face
        So could hard-code each side... or figure out some more general way
        '''
        #z = self._top_position() - self.offset
        z = self.upper_vertex[2] - self.offset
        x_lower,x_upper = self._shrink_range_by_padding(self._x_range())
        y_lower,y_upper = self._shrink_range_by_padding(self._y_range())
        x = random.uniform(x_lower,x_upper)
        y = random.uniform(y_lower,y_upper)
        return x,y,z

    def _get_random_pos_on_a_side(self):
        '''
        how to specify side?
        +x,-x,+y,-y,+z,-z
        '''
        pass

    def _get_random_pos_on_back(self):
        ''' front is defined as the positive most face, along a given axis,
        back is defined as the negative most face,
        '''
        y = self.lower_vertex[1] + self.offset
        x_lower,x_upper = self._shrink_range_by_padding(self._x_range())
        z_lower,z_upper = self._shrink_range_by_padding(self._z_range())
        x = random.uniform(x_lower,x_upper)
        z = random.uniform(z_lower,z_upper)
        return x,y,z

    def _shrink_range_by_padding(self,domain):
        upper,lower = domain
        return lower+self.offset,upper-self.offset 

    def _x_range(self):
        return self.upper_vertex[0],self.lower_vertex[0]

    def _y_range(self):
        return self.lower_vertex[1],self.upper_vertex[1]

    def _z_range(self):
        return self.lower_vertex[2],self.upper_vertex[2]


    def _top_position(self):
        return self.upper_vertex[2]
    
    def front_left(self):
        copy = np.copy(self.lower_vertex)
        np.put(copy,0,self.upper_vertex[0])
        return copy
    
    def x_dimension(self):
        l,u = self._x_range()
        return math.abs(u-l)

    def _range_along(self,axis):
        assert axis in (0,1,2), 'axis was {}, must be one of 0 (x) 1 (y) or 2 (z)'.format(axis)
        return self.lower_vertex[axis], self.upper_vertex[axis]

    def dimension_along(self,axis):
        '''
        axis = (0, 1, 2) representing (x, y, z)
        '''
        l,u = self._range_along(axis)
        return u-l

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
    
    def resize_top(self, new_z, padding=None):
        '''
        resize z dimension of world so that top of box is above
        top of bbox_upper by padding
        '''
        self.upper_vertex[2] = new_z + padding

    def resize_to_fit(self,bbox_lower,bbox_upper,padding=0.0):
        '''
        resize world so that it offsets the box defined by
        bbox_lower and _upper by padding amount
        In all directions except negative z
        '''
        lower_offset = np.array((padding,padding,0.))
        self.lower_vertex = bbox_lower - lower_offset
        upper_offset = np.array([padding]*3)
        self.upper_vertex = bbox_upper + upper_offset

    def get_footprint_area(self):
        ''' gets area of bottom face of box '''
        x = self.dimension_along(0)
        y = self.dimension_along(1)
        return x * y





