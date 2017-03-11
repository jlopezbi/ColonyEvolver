import imp
import cPickle

import plant
import nodes
import brain
import nutrients
import world
imp.reload(plant)
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

class Grower(object):
    def __init__(self,box,particles):
        self.box = box
        self.particles = particles

    @classmethod
    def create_default_grower(cls):
        box = world.BoxWorld((-1.0,-1.0,0.0),(1.0,1.0,1.0))
        num_particles = 60
        particle_sys = nutrients.ParticleSystem(num_particles,box)
        particle_sys.randomness_of_motion = 0.9
        particle_sys.radius = 1.0
        particle_sys.trend_motion_magnitude = .01
        return cls(box,particle_sys)

    def _intialize_to_plant(self,plant):
        self.box.resize_to_fit(plant.bbox.bbox_lower,plant.bbox.bbox_upper,padding=self.particles.radius*self.box.padding_multiplier)
        self.particles.set_initial_positions()

    def report_growth(self,weed):
        box_report = self.box.report()
        weed_report = weed.report()
        print('BoxWorld: ' + box_report)
        print('Plant   : ' + weed_report)

    def grow_from_genome(self,genome,pset,t_steps=100):
        ''' specialized function for genetic programming '''
        func = brain.get_callable(genome,pset)
        seed = seed_stem(func) 
        return self.grow(seed,t_steps)

    def grow(self,seed,t_steps=100):
        '''
        seed is an iterable of node instances, who already have connections between
        them
        '''
        colony = plant.Plant(seed)
        self._intialize_to_plant(weed)
        for i in range(t_steps):
            self.particles.move_particles()
            self.particles.re_spawn_escaped_particles()
            colony .collide_with(self.particles)
            colony .update_time_for_all_nodes()
            self.box.resize_to_fit(weed.bbox.bbox_lower,weed.bbox.bbox_upper,padding=self.particles.radius*self.box.padding_multiplier)
            #self.report_growth(weed)
        return colony 


