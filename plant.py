import bpy
import mathutils
import imp
import numpy as np
import math,random
import inspect
import vector_operations
import mesh_helpers
import numpy_helpers
import metaball_helpers
imp.reload(vector_operations)
imp.reload(numpy_helpers)
imp.reload(mesh_helpers)
imp.reload(metaball_helpers)


'''
notes for development:
custom attributes on a a bmesh vertex:
    http://blender.stackexchange.com/questions/7094/python-assign-custom-tag-to-vertices
    and
    http://blender.stackexchange.com/questions/8992/python-api-custom-properties-for-vertices-edges-faces
'''



class Plant(object):
    """plant composed of nodes"""
    #NOTE: consider making plant a special type of bMesh. might be advantageous for lookup operations

    def __init__(self,start_position):
        #Note: working here
        #IDEA: could have plant be an extended bmesh!
        #obserbation: need to rebuild tree each time a node is added!
        # don't be afraid to do it naively first!

        #first_node = Bud(None,start_position)
        first_node = NodeAwareOfHistory(parent=None,coordinates=start_position,lineage_distance=1)
        self.nodes = [first_node]
        self.mesh_object = mesh_helpers.init_mesh_object()
        mball_obj,mball = metaball_helpers.create_metaball_obj()
        self.mball_obj = mball_obj
        self.mball = mball
        self.bbox_lower = np.array((0.,0.,0.)) 
        self.bbox_upper = np.array((0.,0.,0.))
        #self._init_plant_shape()

    def _init_plant_shape(self):
        '''
        add custom initial geometry to plant
        '''
        idx = 0
        start_vec = np.array((0.0,0.0,1.3))
        parent = self.get_node(idx)
        loc = parent.location + start_vec
        new_node = Node(parent=idx,coordinates=loc)
        self.add_node(new_node)

    def number_of_elements(self):
        return len(self.nodes)
    
    def collide_with(self,particle_system):
        #NOTE: not tested
        '''
        NOTE: this is where an important entanglement between plant
        and nutrients occurs!
        first iteration; knows quite a bit about particle system!
        creates new child nodes fromm nodes that intersect nutrients
        '''
        tree = self._create_spatial_tree()
        particles = particle_system.particles
        for p in particles:
            collided = tree.find_range(p.position,p.radius)
            # returns a list of tuples: (pos,index,dist)
            if not collided:
                continue
            else:
                pos_of_node,index,dist = collided[0]
                #new_node = self.spawn_new_node(p.position,index,dist)
                collided_node = self.get_node(index)
                new_nodes = collided_node.respond_to_collision(self,p.position,p.radius)
                if new_nodes:
                    for node in new_nodes:
                        self.add_node(node)
                particle_system.re_spawn_particle(p)

    def _create_spatial_tree(self):
        '''
        NOTE: the reliance here on mathutils.kdtree is one of the major
        blender dependencies. However, KDTree functionality is readily available from
        other libraries
        Probably would be better to use some sort of spatial tree designed to be dynamically
        grown/updated
        '''
        spatial_tree = mathutils.kdtree.KDTree(self.number_of_elements())
        for i,node in enumerate(self.nodes):
            spatial_tree.insert(node.location,i)
        spatial_tree.balance()
        return spatial_tree

    def get_node(self,node_idx):
        return self.nodes[node_idx]

    def add_node(self,new_node):
        self.nodes.append(new_node)
        self._update_bbox(new_node.location)

    def _update_bbox(self,test_location):
        self.bbox_lower = np.minimum(self.bbox_lower,test_location)
        self.bbox_upper = np.maximum(self.bbox_upper,test_location)

    def _get_parent_node(self,node):
        return self.get_node(node.parent)

    def show(self):
        #for some reason all geometry appears to be parented together in blender
        if len(self.nodes)==1:
            self.nodes[0].show_single(radius=.1)
        else:
            for node in self.nodes:
                node.show(self.mball,self.mesh_object)

    def translate(self,vector):
        '''
        move the blender objects visualizing or skinning this 
        plant. Does not update the actual coordinates of the 
        plant nodes
        '''
        self.mball_obj.location = vector
        self.mesh_object.location = vector

''' NODES'''        
class Node(object):
    '''
    input:
    parent = pointer to an instance of aanother node
    x,y,z = float coordinates of node
    IDEA: node is composed of a graph_tracker, and  responder, and a shower
    '''

    def __init__(self,parent,coordinates,**kwargs):
        if not parent:
            self.parent = self
        else:
            assert type(parent) == Node or inspect.getmro(type(parent))[1] == Node, "parent must be of base-type Node, instead is it of type {}".format(str(type(parent)))
            self.parent = parent
        #self.location = mathutils.Vector(coordinates)
        self.location = np.array(coordinates)
        self.radius = .08
        self._post_initialize(kwargs)

    def _post_initialize(self,kwargs):
        pass
       
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
        return None
        #position = self._new_position_average_internode_sphere_vecs(plant,position)
        #return Node(parent=self,coordinates=position)

    def get_parent_internode_vec(self,plant):
        '''
        gets vector from parent to input node
        '''
        #parent_node = plant.get_node(self.parent)
        parent_node = self.parent
        to_vec = self.location
        from_vec = parent_node.location
        return to_vec-from_vec

    def show(self,mball,mesh_object):
        #self.show_mball_rod(mball)
        self.show_mesh_line(mesh_object)

    def show_mball_rod(self,mball):
        metaball_helpers.add_metaball_rod(mball,self.radius,self.parent.location,self.location)

    def show_mesh_line(self,mesh_object):
        mesh_helpers.add_line_to_mesh_object(mesh_object,self.location,self.parent.location)

    def show_single(self,radius=1.0):
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=radius, location=self.location)

class DumbNode(Node):
    def respond_to_collision(self,plant,position,radius):
        return [DumbNode(parent=self,coordinates=position)]

class SquiggleNode(Node):

    def respond_to_collision(self,plant,position,radius):
        position = self._new_position_average_internode_sphere_vecs(plant,position)
        return [SquiggleNode(parent=self,coordinates=position)]

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

    def respond_to_collision(self,plant,position,radius):
        position = self.weighted_direction(plant,position)
        return [WeightedDirectionNode(parent=self,coordinates=position)]

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
        self.branch_distance = 8 #nodes from branch point before a new branch point occurs
        self.data = []
        self.num_particles_to_grow = 20
        self.internode_weight = .7
        self.collision_weight = .3
        self.is_alive = True

    def respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        enough_hits = len(self.data) >= self.num_particles_to_grow
        if self.distance_from_branch_node >= self.branch_distance and self.is_alive and enough_hits:
            self.is_alive = False
            pos = self.calculate_pos(self.data,plant)
            return [StarBurstBranchNode(parent=self,coordinates=pos)]
        elif enough_hits and self.is_alive:
            self.is_alive = False
            pos = self.calculate_pos(self.data,plant)
            self.data = []
            distance = self.distance_from_branch_node + 1
            return [NodeAwareOfHistory(parent=self,coordinates=pos,lineage_distance=distance)]
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
        self.num_particles_to_grow = 40

    def respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        if len(self.data) >= self.num_particles_to_grow:
            avg_disp = numpy_helpers.get_mean_vector(self.data)
            pos = self.location + avg_disp 
            self.data = []
            return [BranchyNode(parent=self,coordinates=pos)]
            self.num_particles_to_grow = 3
            #return [Bud(parent=self,coordinates=pos)]
        else:
            return None

    def create_branches(self,plant,number):
        internode_vec = self.get_parent_internode_vec(plant)

class BudSub(Node):
    def _post_initialize(self,args):
        self.data = []
        self.num_particles_to_grow = 3

    def respond_to_collision(self,plant,position,radius):
        vec_disp = position - self.location 
        self.data.append(vec_disp)
        if len(self.data) >= self.num_particles_to_grow:
            avg_disp = numpy_helpers.get_mean_vector(self.data)
            pos = self.location + avg_disp 
            self.data = []
            return [BranchyNode(parent=self,coordinates=pos)]
            #return [Bud(parent=self,coordinates=pos)]
        else:
            return None

    def create_branches(self,plant,number):
        internode_vec = self.get_parent_internode_vec(plant)


class StarBurstBranchNode(Node):
    def _post_initialize(self,kwargs):
        self.hits = 0
        self.num_particles_to_grow = 1
        self.number_branches = 5
        self.is_alive = True

    def respond_to_collision(self,plant,position,radius):
        self.hits +=1
        if self.enough_hits() and self.is_alive:
            self.is_alive = False
            axis = self.get_parent_internode_vec(plant)
            ortho = vector_operations.get_ortho(axis)
            vecs = vector_operations.make_star_burst(ortho,axis,self.number_branches)
            new_nodes = []
            for v in vecs:
                pos = np.array(v) + self.location
                new_nodes.append(NodeAwareOfHistory(parent=self,coordinates=pos,lineage_distance=1))
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

    def respond_to_collision(self,plant,position,radius):
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
            #return [BranchyNode(parent=self,coordinates=pos1),BranchyNode(parent=self,coordinates=pos2)]
            #return [Bud(parent=self,coordinates=pos1),Bud(parent=self,coordinates=pos2)]
            #return [Bud(parent=self,coordinates=pos1)]
            return [NodeAwareOfHistory(parent=self,coordinates=pos1,lineage_distance=1),NodeAwareOfHistory(parent=self,coordinates=pos2,lineage_distance=1),NodeAwareOfHistory(parent=self,coordinates=pos3,lineage_distance=1)]
        else:
            return None

    def get_branch_pos(self,plant):
        o = self.get_branch_ortho_rand(plant)
        return self.location + o

    def get_branch_ortho_rand(self,plant):
        internode_vec = mathutils.Vector(self.get_parent_internode_vec(plant))
        ortho_rand = internode_vec.orthogonal()
        ortho_rand.normalize()
        angle = random.uniform(0.0,math.pi*2)
        ortho_rand.rotate(self.create_rotation_quat(internode_vec,angle))
        n = ortho_rand * internode_vec.length  
        return n

    def create_rotation_quat(self,vector,angle):
        return mathutils.Quaternion(vector,angle)



def _grow_cone_position(base_vector,input_vector,radius):
    '''
    \  / 
     \/
      
    finds a vector inside or on the cone defined by base_vector
    and radius. If the input vector position lies outside the cone, the position
    is clamped to the cone surface
    '''


