import imp
import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt
import math,random
import inspect
import visualization_base as vb

import collisions
import base_objects
import numpy_helpers
import nodes
import mayavi.mlab as mlab
imp.reload(collisions)
#imp.reload(base_objects)
#imp.reload(numpy_helpers)
#imp.reload(nodes)


class Colony(object):
    """colony composed of nodes, a bounding box
    seed_nodes = iterable collection of obects derived from Node
    Note that seed_nodes must already have parent relations setup amongst themselves
    """


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
        #return np.sum(scores)

    ## Interesting Note: ##
    # returning the average results in ~inverse relationship between health and # of nodes
    # returning the sum results in ~negative linear relationship between health and # of nodes

    def collide_with(self,particle_sys):
        #self.collide_with_array_node_view(particle_sys)
        #self.collide_with_single_version(particle_sys)
        self.collide_with_arr_particle_view(particle_sys)

    def collide_with_arr_particle_view(self,particle_sys):
        '''
        fastest thus far method for computing collisions
        computes collisions for particles. For each collisions set of a particle,
        arbitrarily chooses a node to grow.
        '''
        particles_tree = sp.cKDTree(particle_sys.get_matrix_form())
        colony_tree = sp.cKDTree(self.get_matrix_form())
        radius = particle_sys.radius
        neighbor_array = particles_tree.query_ball_tree(colony_tree, radius)
        for i,nodes in enumerate(neighbor_array):
            if nodes:
                p = particle_sys.get_particle(i)
                n_idx = nodes[0] #arbitrary choice
                position = particles_tree.data[i]
                collided_node = self.nodes[n_idx]
                new_nodes = collided_node.respond_to_collision(self,position,radius)
                if new_nodes:
                    for node in new_nodes:
                        self.append_node(node, collided_node)
                particle_sys.re_spawn_particle(p)

    def collide_with_array_node_view(self,particle_sys):
        '''test if faster.'''
        #There is an inherent diffuclty here: nothing stops two nodes from being
        #fed by the same particle. In the other version collided particles get respawned.
        #here the data of the collision remains unchanged!
        #would make sense to prefer node that is closest to center of particle!
        #IDEA: flip the collision, so that is from the particles perspective.
        #foreach particle decide which node gets fed, and then discount others from feeding
        colony_tree = collisions.create_spatial_tree(self.get_matrix_form())
        particles_tree = collisions.create_spatial_tree(particle_sys.get_matrix_form())
        radius = particle_sys.radius
        neighbor_array = collisions.collide(colony_tree, particles_tree, radius)
        for i,positions in enumerate(neighbor_array):
            if positions:
                collided_node = self.nodes[i]
                p_idx = positions[0] #arbitrarily grab first particleindex
                p = particle_sys.get_particle(p_idx)
                position = particles_tree.data[p_idx]
                new_nodes = collided_node.respond_to_collision(self, position, p.radius)
                if new_nodes:
                    for node in new_nodes:
                        self.append_node(node, collided_node)
                particle_sys.re_spawn_particle(p)

    def collide_with_single_version(self,particle_system):
        '''
        find collisions of self with particle_system,
        send message to collided nodes to respond to collision
        '''
        tree = self._create_spatial_tree()
        particles = particle_system.particles
        for p in particles:
            neighbors = tree.query_ball_point(p.position,p.radius)
            #neighbors is an array of lists of indices 
            #that correspond to points in the tree.
            #in this case that means plant nodes
            if not neighbors:
                continue
            else:

                index = neighbors[0]
                #for now just take first neighbor, to simplify stuff
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
        creates spatial tree used for efficiently computing collisions
        '''
        spatial_tree = sp.cKDTree(self.get_matrix_form())
        return spatial_tree

    def get_matrix_form(self):
        '''returns matrix of points making up colony, shape: Npoints x 3 (x,y,z)'''
        vectors = self.get_node_vectors()
        return np.stack(vectors,axis=0)

    def get_node_vectors(self):
        return [node.location for node in self.nodes]

    def get_node(self,node_idx):
        return self.nodes[node_idx]

    def get_index_for_node(self,node):
        return self.nodes.index(node)

    def append_node(self,new_node,old_node=None):
        '''
        adds new node, then adds mesh, then updates bbox
        Perhaps dangerous function that hides alot!
        '''
        self.nodes.append(new_node)
        self.bbox.update_bbox(new_node.location)

    def show_indvidual_calls(self, fig=None):
        '''depricated, less efficient drawing'''
        for node in self.nodes:
            node.show(fig)

    def show(self,fig=None):
        auto_show = False
        if fig==None:
            auto_show = True
            fig = vb.init_fig()
        self.show_lines()
        if auto_show:
            vb.show_fig()

    def show_lines(self):
        x, y, z, connections = self.collect_line_data()
        vb.make_lines(x, y, z, connections)
    
    def save_image(self,info,img_name="colony.png"):
        self.show_lines()
        mlab.text(x=.01, y=.01, text=info, width=0.9)
        mlab.savefig(img_name)
        mlab.close(all=True)

    def collect_line_data(self):
        x = []
        y = []
        z = []
        connections = []
        for node_idx, node in enumerate(self.nodes):
            x_loc, y_loc, z_loc = node.location
            x.append(x_loc)
            y.append(y_loc)
            z.append(z_loc)
            parent_idx = self.get_index_for_node(node.parent)
            connections.append([parent_idx, node_idx])
        #Cast to numpy arrays
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        connections = np.array(connections)
        return x, y, z, connections

    def save_line_data(self):
        x,y,z,c = self.collect_line_data()
        data = {'x':x, 'y':y, 'z':z, 'connections':c}
        np.save('line_data.npy',data)

    def translate(self,vector):
        '''
        move the blender objects visualizing or skinning this 
        plant. Does not update the actual coordinates of the 
        plant nodes
        '''
        #self.mball_obj.location = vector
        if self.object_linked:
            self.object_linked.location = vector


