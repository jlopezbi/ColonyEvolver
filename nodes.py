#import mathutils
import imp
import numpy as np
import matplotlib.pyplot as plt
import math,random
import inspect
import vector_operations
#import mesh_helpers
import numpy_helpers
#import metaball_helpers
import brain
import mayavi.mlab as mlab
imp.reload(vector_operations)
imp.reload(numpy_helpers)
imp.reload(brain)

class Node(object):
    '''input:
    parent = pointer to an instance of aanother node
    location = float location of node
    kwargs = additional arguments for nodes which are derived from Node
    '''

    def __init__(self, parent=None, location=(0.0,0.0,0.0) , **kwargs):
        if not parent:
            self.parent = self
        else:
            assert type(parent) == Node or inspect.getmro(type(parent))[-2] == Node, "parent must be of base-type Node, instead is it of type {}".format(str(type(parent)))
            self.parent = parent
        self.location = np.array(location )
        self.radius = .08
        self._post_initialize(kwargs)
        self.health = 5

    def _post_initialize(self,kwargs):
        pass
    
    def make_self_child(self,location,**kwargs):
        #NOTE: working here
        node_class = self.__class__
        return node_class(self,location,**kwargs)
       
    def respond_to_collision(self,plant,position,radius):
        '''
        Template function that gets called when this node gets hit by a particle
        dpending on the node type any number of things could happen:
            - increase a number
            - store some data
            - create a new node
            - delete self
            - move self's position
            - affect all parents
            - affect all children
        '''
        self.health +=5

        new_nodes = self._specialized_respond_to_collision(plant,position,radius)
        return new_nodes

    def time_passed(self):
        '''
        function called by simulation to let the node know that time has passed
        '''
        self.health -=2

    def _specialized_respond_to_collision(self,plant,position,radius):
        '''
        to be overwritten by derivitative nodes
        '''
        return [None]

    def parent_chain_message(self,*args):
        self.parent_chain_action(args)
        if self.parent != self:
            self.parent.parent_chain_message(args)

    def parent_chain_action(self,args):
        pass

    def get_parent_internode_vec(self,plant):
        '''
        gets vector from parent to input node
        '''
        #parent_node = plant.get_node(self.parent)
        parent_node = self.parent
        to_vec = self.location
        from_vec = parent_node.location
        return to_vec-from_vec

    def get_line(self):
        p1 = self.location
        p2 = self.parent.location
        stack = np.stack([p2,p1],axis=1)
        return stack
        #x = stack[0]
        #y = stack[1]
        #z = stack[2]
        #return x, y, z

# if doing many calls to plot3d is less efficient than doing
# one call what would be the hint? I really think it makes sense to simply try both out!

    def show(self,fig):
        coords = self.get_line()
        x = coords[0]
        y = coords[1]
        z = coords[2]
        #draw line
        #mlab.plot3d(x, y, z, tube_radius=.012)
        mlab.plot3d(x, y, z, figure=fig, line_width=1.0)
        #draw dot
        #mlab.points3d(x[0],y[0],z[0], figure=fig, mode='sphere',scale_factor=.08)

    def show_mball_rod(self,mball):
        #metaball_helpers.add_metaball_rod(mball,self.radius,self.parent.location,self.location)
        pass

    def show_mesh_line(self,mesh_object):
        pass
        #mesh_helpers.add_line_to_mesh_object(mesh_object,self.location,self.parent.location)

    def show_single(self,radius=1.0):
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=radius, location=self.location)

'''Derived Nodes'''
class DumbNode(Node):
    def _specialized_respond_to_collision(self,plant,position,radius):
        return [DumbNode(parent=self,location =position)]

class SquiggleNode(Node):

    def _specialized_respond_to_collision(self,plant,position,radius):
        position = self._new_position_average_internode_sphere_vecs(plant,position)
        return [SquiggleNode(parent=self,location =position)]

    def _new_position_average_internode_sphere_vecs(self,plant,pos_vec):
        '''
        determine where the new node should be
        given the position of the sphere, the node it intersected
        and its distance to that node
        '''
        parent_node = self.parent
        internode_vec = self.get_parent_internode_vec(plant)
        #note using parent node location! this is what makes it more squiggly
        node_to_sphere = np.array(pos_vec)-parent_node.location 
        displacement = numpy_helpers.get_mean_vector((internode_vec,node_to_sphere))
        return displacement + parent_node.location

class WeightedDirectionNode(Node):

    def _specialized_respond_to_collision(self,plant,position,radius):
        position = self.weighted_direction(plant,position)
        return [WeightedDirectionNode(parent=self,location =position)]

    def weighted_direction(self,plant,position):
        parent_node = self.parent
        internode_vec = self.get_parent_internode_vec(plant)
        node_to_sphere = np.array(position)-self.location
        weights = (.95,.05)
        displacement = numpy_helpers.get_weighted_average_vectors((internode_vec,node_to_sphere),weights)
        return displacement + self.location

class NodeAwareOfHistory(Node):
    '''
    branching after some number of nodes get added from a previous branch point
    '''
    def _post_initialize(self,kwargs):
        self.distance_from_branch_node = kwargs['lineage_distance']
        self.branch_distance = 5 #nodes from branc point before a new branch point occurs
        self.data = []
        self.num_particles_to_grow = 20
        self.internode_weight = .7
        self.collision_weight = .3
        self.is_alive = True

    def _specialized_respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        enough_hits = len(self.data) >= self.num_particles_to_grow
        if self.distance_from_branch_node >= self.branch_distance and self.is_alive and enough_hits:
            self.is_alive = False
            pos = self.calculate_pos(self.data,plant)
            return [StarBurstBranchNode(parent=self,location =pos)]
        elif enough_hits and self.is_alive:
            self.is_alive = False
            pos = self.calculate_pos(self.data,plant)
            self.data = []
            distance = self.distance_from_branch_node + 1
            return [NodeAwareOfHistory(parent=self,location =pos,lineage_distance=distance)]
        else:
            return None

    def calculate_pos(self,data,plant):
        avg_disp = numpy_helpers.get_mean_vector(self.data)
        pos = self.location + avg_disp 
        parent_node = self.parent
        internode_vec = self.get_parent_internode_vec(plant)
        weights = (self.internode_weight,self.collision_weight)
        displacement = numpy_helpers.get_weighted_average_vectors((internode_vec,avg_disp),weights)
        return displacement + self.location

class Bud(Node):
    def _post_initialize(self,args):
        self.data = []
        self.num_particles_to_grow = 5
        self.radius = .01
        self.radius_growth_step = .01

    def _specialized_respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        if len(self.data) >= self.num_particles_to_grow:
            avg_disp = numpy_helpers.get_mean_vector(self.data)
            pos = self.location + avg_disp 
            self.data = []
            #return [BranchyNode(parent=self,location =pos)]
            self.parent_chain_message()
            self.num_particles_to_grow = 40
            return [Bud(parent=self,location =pos)]
        else:
            return None

    def parent_chain_action(self,*args):
        self.radius += self.radius_growth_step

    def create_branches(self,plant,number):
        internode_vec = self.get_parent_internode_vec(plant)

class BudSub(Node):
    def _post_initialize(self,args):
        self.data = []
        self.num_particles_to_grow = 40

    def _specialized_respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        if len(self.data) >= self.num_particles_to_grow:
            avg_disp = numpy_helpers.get_mean_vector(self.data)
            pos = self.location + avg_disp 
            self.data = []
            #return [BranchyNode(parent=self,location =pos)]
            return [Bud(parent=self,location =pos)]
        else:
            return None

    def create_branches(self,plant,number):
        internode_vec = self.get_parent_internode_vec(plant)

class StarBurstBranchNode(Node): 
    def _post_initialize(self,kwargs):
        self.hits = 0
        self.num_particles_to_grow = 15
        self.number_branches = 7
        self.is_alive = True

    def _specialized_respond_to_collision(self,plant,position,radius):
        self.hits +=1
        if self.enough_hits() and self.is_alive:
            self.is_alive = False
            axis = self.get_parent_internode_vec(plant)
            ortho = vector_operations.get_ortho(axis)
            ortho = vector_operations.rotate_vec(ortho,axis,random.uniform(0,math.pi*2.0))
            vecs = vector_operations.make_star_burst(ortho,axis,self.number_branches)
            new_nodes = []
            for v in vecs:
                pos = np.array(v) + self.location
                new_nodes.append(NodeAwareOfHistory(parent=self,location =pos,lineage_distance=1))
            
            return new_nodes
        else:
            return None

    def enough_hits(self):
        return self.hits >= self.num_particles_to_grow

class BranchyNode(Node):
    def _post_initialize(self,args):
        self.data = []
        self.num_particles_to_grow = 1
        self.did_run = False

    def _specialized_respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        if len(self.data) >= self.num_particles_to_grow and not self.did_run:
            avg_disp = numpy_helpers.get_mean_vector(self.data)
            pos = self.location + avg_disp 
            self.data = []
            pos1 = self.get_branch_pos(plant)
            pos2 = self.get_branch_pos(plant)
            pos3 = self.get_branch_pos(plant)
            self.did_run = True
            #return [BranchyNode(parent=self,location =pos1),BranchyNode(parent=self,location =pos2)]
            #return [Bud(parent=self,location =pos1),Bud(parent=self,location =pos2)]
            #return [Bud(parent=self,location =pos1)]
            return [NodeAwareOfHistory(parent=self,location =pos1,lineage_distance=1),NodeAwareOfHistory(parent=self,location =pos2,lineage_distance=1),NodeAwareOfHistory(parent=self,location =pos3,lineage_distance=1)]
        else:
            return None

    def get_branch_pos(self,plant):
        o = self.get_branch_ortho_rand(plant)
        return self.location + o

    def get_branch_ortho_rand(self,plant):
        #NOTE: need to replace with vector_operations code
        '''
        internode_vec = mathutils.Vector(self.get_parent_internode_vec(plant))
        ortho_rand = internode_vec.orthogonal()
        ortho_rand.normalize()
        angle = random.uniform(0.0,math.pi*2)
        ortho_rand.rotate(self.create_rotation_quat(internode_vec,angle))
        n = ortho_rand * internode_vec.length  
        '''
        pass

    def create_rotation_quat(self,vector,angle):
        #return mathutils.Quaternion(vector,angle)
        pass

#TODO: figure out how to make a node lineage that has one type of processor
#also make sure that processor is getting regenerated when I want it to!
#hmmm some class stuffs...

class BrainNode(Node):

    def _post_initialize(self,kwargs):
        self.processor = kwargs['processor']

    def _specialized_respond_to_collision(self,plant,position,radius):
        node_to_sphere = position - self.location 
        parent_to_node = self.get_parent_internode_vec(plant)
        if not parent_to_node.any():
            return None
        new_offset = self.processor(node_to_sphere,parent_to_node)
        z = np.array([0.0, 0.0, 0.0])
        if np.isclose(z,new_offset,atol=.01).all() or np.isnan(new_offset).any():
            return None
        new_position = self.location + new_offset
        return [BrainNode(parent=self,location=new_position,processor=self.processor)]


def _grow_cone_position(base_vector,input_vector,radius):
    '''
    \  / 
     \/
      
    finds a vector inside or on the cone defined by base_vector
    and radius. If the input vector position lies outside the cone, the position
    is clamped to the cone surface
    '''


