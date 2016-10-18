import bpy
import mathutils
import imp
import numpy as np
import mesh_helpers
imp.reload(mesh_helpers)
#TODO: 
# - clean up this module
#probably should be a base-class for plant upon which various growth behaviors are added
# - add plants that have constant branching direction
# - plants that have different types of nodes

'''
notes for development:
custom attributes on a a bmesh vertex:
    http://blender.stackexchange.com/questions/7094/python-assign-custom-tag-to-vertices
    and
    http://blender.stackexchange.com/questions/8992/python-api-custom-properties-for-vertices-edges-faces
'''

def get_average_vector(vectors):
    '''
    vectors must be tuple of np.array() with only one dimension
    all vectors must be same size
    '''
    c = np.column_stack(vectors)
    return np.mean(c,axis=1)


class Plant(object):
    """plant composed of nodes"""
    #NOTE: look into making plant a special type of bMesh. might be advantageous for lookup operations

    def __init__(self,start_position):
        #Note: working here
        #IDEA: could have plant be an extended bmesh!
        #obserbation: need to rebuild tree each time a node is added!
        # don't be afraid to do it naively first!

        first_node = Node(0,start_position)
        self.nodes = [first_node]
        self.mesh_object = mesh_helpers.init_mesh_object()
        self.bbox_lower = np.array((0.,0.,0.)) 
        self.bbox_upper = np.array((0.,0.,0.))
        self._init_plant_shape()

    def _init_plant_shape(self):
        '''
        add custom initial geometry to plant
        '''
        idx = 0
        start_vec = np.array((0.0,0.0,1.3))
        parent = self.get_node(idx)
        loc = parent.location + start_vec
        new_node = Node(parent=idx,coordinates=loc)
        self._add_node(new_node)

    def number_of_elements(self):
        return len(self.nodes)
    
    def grow_collided(self,particles):
        '''
        first iteration 
        creates new child nodes fromm nodes that intersect nutrients
        '''
        tree = self._create_spatial_tree()
        for p in particles:
            collided = tree.find_range(p.position,p.radius)
            # returns a list of tuples: (pos,index,dist)
            if not collided:
                continue
            else:
                pos_of_node,index,dist = collided[0]
                new_node = self.spawn_new_node(p.position,index,dist)
                self._add_node(new_node)

    def _create_spatial_tree(self):
        spatial_tree = mathutils.kdtree.KDTree(self.number_of_elements())
        for i,node in enumerate(self.nodes):
            spatial_tree.insert(node.location,i)
        spatial_tree.balance()
        return spatial_tree

    def spawn_new_node(self,pos_vec,node_idx,dist):
        '''
        create new node
        pos_vec = position of sphere
        node_idx = parent node
        dist = distance from parent node to sphere
        '''
        location = self._get_new_node_position(pos_vec,node_idx)
        return Node(parent=node_idx,coordinates=location)
    
    def _get_new_node_position(self,pos_vec,node_idx):
        '''
        NOTe: should be renamed to get average between internode 
        and sphere position
        determine where the new node should be
        given the position of the sphere, the node it intersected
        and its distance to that node
        '''
        parent_node = self.get_node(node_idx)
        internode_vec = self.get_parent_internode_vec(node_idx)
        node_to_sphere = np.array(pos_vec)-parent_node.location
        displacement = get_average_vector((internode_vec,node_to_sphere))
        return displacement + parent_node.location


    def get_parent_internode_vec(self,node_idx):
        '''
        gets vector from parent to input node
        '''
        node = self.get_node(node_idx)
        to_vec = node.location
        from_vec = self._get_parent_node(node).location
        return to_vec-from_vec

    def get_node(self,node_idx):
        return self.nodes[node_idx]

    def _add_node(self,new_node):
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
            self.nodes[0].show(radius=.1)
        else:
            for node in self.nodes:
                parent_node = self._get_parent_node(node)
                mesh_helpers.add_line_to_mesh_object(self.mesh_object,node.location,parent_node.location)

class Node(object):
    '''
    input:
    parent = pointer to another node
    x,y,z = float coordinates of node
    '''

    def __init__(self,parent,coordinates):
        self.parent = parent
        #self.location = mathutils.Vector(coordinates)
        self.location = np.array(coordinates)

    def show(self,radius=1.0):
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=radius, location=self.location)

    def spawn_child(self,):
        pass
