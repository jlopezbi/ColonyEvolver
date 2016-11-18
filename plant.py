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
import nodes
imp.reload(vector_operations)
imp.reload(numpy_helpers)
imp.reload(mesh_helpers)
imp.reload(metaball_helpers)
imp.reload(nodes)


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
        first_node = nodes.NodeAwareOfHistory(parent=None,coordinates=start_position,lineage_distance=1)
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


