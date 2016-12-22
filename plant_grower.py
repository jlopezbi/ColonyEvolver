import sys,os,imp
import bpy
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)

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
        self.box.resize_to_fit(plant.bbox_lower,plant.bbox_upper,padding=self.particles.radius*self.box.padding_multiplier)
        self.particles.set_initial_positions()

    def report_growth(self,weed):
        box_report = self.box.report()
        print('BoxWorld: ' + box_report)

    def grow(self,seed,t_steps=100):
        weed = plant.Plant(seed)
        self._intialize_to_plant(weed)
        for i in range(t_steps):
            self.particles.move_particles()
            self.particles.re_spawn_escaped_particles()
            weed.collide_with(self.particles)
            self.box.resize_to_fit(weed.bbox_lower,weed.bbox_upper,padding=self.particles.radius*self.box.padding_multiplier)
            self.report_growth(weed)
        return weed


