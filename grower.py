import imp
import cPickle

import colony_class
import nodes
import brain
import nutrients
import world
imp.reload( colony_class )
imp.reload(nodes)
imp.reload(brain)
imp.reload(nutrients)
imp.reload(world)

def create_seed(func):
    return nodes.BrainNode(processor=func)

def seed_stem(func):
    base = nodes.BrainNode(location=(0.,0.,0.), processor=func)
    end = nodes.BrainNode(parent=base, location=(0.0,0.0,0.5), processor=func)
    return [base,end]

def save(colony):
    #not tested yet!
    pickle.dump(colony, open('pickled_colony.p', 'wb'))

def load(filename):
    #not tested yet! 
    pickle.load(open(filename, 'rb'))

class EvenNutrientsGrower(object):
    '''
    Designed to give amount of nutrients proportional to the
    area of the footprint of the world.
    As the footprint increases, more particles are added to 
    maintian the particle-to-footprint_area ratio.
    ASSUMPTION:
        world always increaeses footprint area, never decreases
        (will never remove particles after they have been added)
    Expect a ratio of num_particles:footprint_area that saw-tooths below some 
    target ratio over the course of the sim. That ratio is set in nutrients 
    (get_n_particles_per_area) 
    '''

    def __init__(self):
        f = .1 #box will get resized to seed
        box = world.BoxWorld((-f,-f,0.0),(f,f,f))
        self.start_particles = 2
        particle_sys = nutrients.ParticleSystem(box)
        particle_sys.randomness_of_motion = 0.9
        particle_sys.radius = 1.0
        particle_sys.trend_motion_magnitude = .01
        particle_sys.finalize()
        self.box = box
        self.particles = particle_sys

    def resize_box_to_colony(self, colony):
        colony_lower = colony.bbox.bbox_lower
        colony_upper = colony.bbox.bbox_upper
        extra_space = self.particles.radius*self.box.padding_multiplier
        self.box.resize_to_fit(colony_lower, colony_upper, padding=extra_space)
        return self.box.get_footprint_area()

    def grow(self, seed, t_steps=20):
        colony = colony_class.Colony(seed)
        self.resize_box_to_colony(colony)
        self.particles.add_n_particles_at_spawn_loc(self.start_particles)
        for i in range(t_steps):
            self.particles.move_particles()
            self.particles.re_spawn_escaped_particles()
            colony.collide_with(self.particles)
            colony.update_time_for_all_nodes()
            self.resize_box_to_colony(colony)
            self.particles.add_missing_particles_if_required()
        return colony

class FixedFootprintGrower(object):
    def __init__(self, base_width=5):
        hw = base_width/2.0
        box = world.BoxWorld( (-hw, -hw, 0.0), (hw, hw, 15.0) )
        num_particles = 60
        particle_sys = nutrients.ParticleSystem(box)
        particle_sys.randomness_of_motion = 0.9
        particle_sys.radius = 1.0
        particle_sys.trend_motion_magnitude = .01
        particle_sys.add_n_particles_at_spawn_loc(num_particles)
        self.box = box
        self.particles = particle_sys

    def grow(self, seed, t_steps=20):
        '''resized top of box world only '''
        colony = colony_class.Colony(seed)
        self.box.resize_top(colony.bbox.bbox_upper[2], padding=self.particles.radius*self.box.padding_multiplier)
        self.particles.set_initial_positions()
        for i in range(t_steps):
            self.particles.move_particles()
            self.particles.re_spawn_escaped_particles()
            colony.collide_with(self.particles)
            colony.update_time_for_all_nodes()
            self.box.resize_top(colony.bbox.bbox_upper[2], padding=self.particles.radius*self.box.padding_multiplier)
        return colony

class Grower(object):
    def __init__(self,box,particles):
        self.box = box
        self.particles = particles

    @classmethod
    def create_default_grower(cls):
        box = world.BoxWorld((-1.0,-1.0,0.0),(1.0,1.0,1.0))
        num_particles = 60
        particle_sys = nutrients.ParticleSystem(box)
        particle_sys.randomness_of_motion = 0.9
        particle_sys.radius = 1.0
        particle_sys.trend_motion_magnitude = .01
        particle_sys.add_n_particles_at_spawn_loc(num_particles)
        return cls(box,particle_sys)

    @classmethod
    def create_fixed_footprint_grower(cls):
        width = 5.0
        hw = width/2.0
        box = world.BoxWorld( (-hw, -hw, 0.0), (hw, hw, 15.0) )
        num_particles = 60
        particle_sys = nutrients.ParticleSystem(box)
        particle_sys.randomness_of_motion = 0.9
        particle_sys.radius = 1.0
        particle_sys.trend_motion_magnitude = .01
        particle_sys.add_n_particles_at_spawn_loc(num_particles)
        return cls(box,particle_sys)
    

    def _intialize_to_plant(self, colony):
        self.box.resize_to_fit( colony.bbox.bbox_lower, colony.bbox.bbox_upper,padding=self.particles.radius*self.box.padding_multiplier)
        self.particles.set_initial_positions()

    def report_growth(self,weed):
        box_report = self.box.report()
        weed_report = weed.report()
        print('BoxWorld: ' + box_report)
        print('Colony   : ' + weed_report)

    def grow_from_genome(self,genome,pset,t_steps=100):
        ''' specialized function for genetic programming '''
        func = brain.get_callable(genome,pset)
        seed = seed_stem(func) 
        return self.grow(seed,t_steps)

    def grow_resize_top(self, seed, t_steps=100):
        colony = colony_class.Colony(seed)
        self.box.resize_top(colony.bbox.bbox_upper[2], padding=self.particles.radius*self.box.padding_multiplier)
        self.particles.set_initial_positions()
        for i in range(t_steps):
            self.particles.move_particles()
            self.particles.re_spawn_escaped_particles()
            colony.collide_with(self.particles)
            colony.update_time_for_all_nodes()
            self.box.resize_top(colony.bbox.bbox_upper[2], padding=self.particles.radius*self.box.padding_multiplier)
        return colony

    def grow(self,seed,t_steps=100):
        '''
        seed is an iterable of node instances, who already have connections between
        them
        '''
        colony = colony_class.Colony(seed)
        self._intialize_to_plant(colony)
        for i in range(t_steps):
            self.particles.move_particles()
            self.particles.re_spawn_escaped_particles()
            colony.collide_with(self.particles)
            colony.update_time_for_all_nodes()
            self.box.resize_to_fit(colony.bbox.bbox_lower,colony.bbox.bbox_upper,padding=self.particles.radius*self.box.padding_multiplier)
            #self.report_growth(colony)
        return colony 

def defualt_plant():
    n0 = nodes.Node(location=(0.0, 0.0, 0.0))
    p = colony.Colony([n0])
    n1 = nodes.Node(parent=n0, location=(0.0, 0.0, 5.0))
    p.append_node(n1,n0)
    n2 = nodes.Node(parent=n0, location=(4.0, 0.0, 5.0))
    p.append_node(n2,n0)
    return p


