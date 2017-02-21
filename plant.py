import mathutils
import imp
import numpy as np
import scipy.spatial as sp
import math,random
import inspect

import base_objects
import numpy_helpers
import nodes
imp.reload(base_objects)
imp.reload(numpy_helpers)
imp.reload(nodes)

class Plant(object):
    """plant composed of nodes, a bounding box
    seed_nodes = iterable collection of obects derived from Node
    Note that seed_nodes must already have parent relations setup amongst themselves
    In This version Plant has a mesh_grower, so Plant is responsible for constructing the visualization"""

    def __init__(self,seed_nodes):
        #IDEA: could have plant be an extended bmesh!
        #obserbation: need to rebuild tree each time a node is added!
        # don't be afraid to do it naively first!

        #self.mesh_object = mesh_helpers.init_mesh_object()
        self.object_linked = None
        #self.mball = mball
        self.bbox = base_objects.BoundingBox()
        self.nodes = []
        try:
            prev_node = None
            for node in seed_nodes:
                self.append_node(node,prev_node)
                prev_node = node
        except TypeError:
            self.append_node(seed_nodes)

    def number_of_elements(self):
        return len(self.nodes)

    def update_time_for_all_nodes(self):
        '''
        naively iterates through all nodes and tells
        node that time passed
        '''
        for node in self.nodes:
            node.time_passed()

    def get_health(self):
        scores = []
        for n in self.nodes:
            scores.append(n.health)
        return np.average(scores)

    def collide_with(self,particle_system):
        '''
        NOTE: this is where an important entanglement between plant
        and nutrients occurs!
        first iteration; knows quite a bit about particle system!
        creates new child nodes fromm nodes that intersect nutrients
        '''
        tree = self._create_spatial_tree()
        particles = particle_system.particles
        for p in particles:
            #NOTE: working here update to match new kdtree (scipy)
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
                        self.append_node(node,collided_node)
                particle_system.re_spawn_particle(p)

    def report(self):
        nodes_report = 'number of nodes: ' + str(len(self.nodes))
        size_report = 'bbox: ' + str(self.bbox.bbox_lower) + str(self.bbox.bbox_upper)
        report_string = nodes_report + '\n' + size_report
        return size_report

    def _create_spatial_tree(self):
        '''
        NOTE: the reliance here on mathutils.kdtree is one of the major
        blender dependencies. However, KDTree functionality is readily available from
        other libraries
        Probably would be better to use some sort of spatial tree designed to be dynamically
        grown/updated
        '''
        spatial_tree = sp.cKDTree(self.get_matrix_form())
        return spatial_tree

    def get_matrix_form(self):
        vectors = self.get_node_vectors()
        return np.stack(vectors,axis=0)

    def get_node_vectors(self):
        return [node.location for node in self.nodes]

    def get_node(self,node_idx):
        return self.nodes[node_idx]

    def append_node(self,new_node,old_node=None):
        '''
        adds new node, then adds mesh, then updates bbox
        Perhaps dangerous function that hides alot!
        '''
        self.nodes.append(new_node)
        self.bbox.update_bbox(new_node.location)

    def show(self):
        #for some reason all geometry appears to be parented together in blender
        #print("Nothing hooked up to show plant yet")
        pass

    def translate(self,vector):
        '''
        move the blender objects visualizing or skinning this 
        plant. Does not update the actual coordinates of the 
        plant nodes
        '''
        #self.mball_obj.location = vector
        if self.object_linked:
            self.object_linked.location = vector


