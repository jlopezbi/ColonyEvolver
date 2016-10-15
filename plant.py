import bpy
import mathutils
import imp
import mesh_helpers
imp.reload(mesh_helpers)

'''
notes for development:
custom attributes on a a bmesh vertex:
    http://blender.stackexchange.com/questions/7094/python-assign-custom-tag-to-vertices
    and
    http://blender.stackexchange.com/questions/8992/python-api-custom-properties-for-vertices-edges-faces
'''

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
                pos_vec,index,dist = collided[0]
                new_node = Node(index,p.position)
                self._add_node(new_node)

    def _create_spatial_tree(self):
        spatial_tree = mathutils.kdtree.KDTree(self.number_of_elements())
        for i,node in enumerate(self.nodes):
            spatial_tree.insert(node.location,i)
        spatial_tree.balance()
        return spatial_tree
    
    def _add_node(self,new_node):
        self.nodes.append(new_node)

    def _get_parent_node(self,node):
        return self.nodes[node.parent]

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
        self.location = mathutils.Vector(coordinates)

    def show(self,radius=1.0):
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=radius, location=self.location)

    def spawn_child(self,):
        pass
