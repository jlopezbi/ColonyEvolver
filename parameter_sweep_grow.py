import sys,os,imp
import bpy
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)
import numpy as np

#import simrunner #not built yet

import plant
import nutrients
import world
imp.reload(plant)
imp.reload(nutrients)
imp.reload(world)

'''
param_name = 'randomness_of_motion'
randomness_of_motion = np.arange(0.0,1.0,0.1)
sweeper = simrunner.ParameterSweeper(randomness_of_motion,param_name)
'''

randomness_of_motion = np.arange(0.0,1.0,0.1)
steps = 70
parameter_range = randomness_of_motion
pos_vector = np.array((0.,0.,0.))
for p in parameter_range:
    '''set up'''
    side = 2.0
    height = 3.0 
    front = (-side/2,-side/2,0.0)
    back = (side/2,side/2,height)
    box = world.BoxWorld(front,back)

    num_particles = 60
    particle_system = nutrients.ParticleSystem(num_particles,box)
    # swept paremater
    particle_system.randomness_of_motion = p
    particle_system.radius = 1.2
    particle_system.trend_motion_magnitude = 1.0

    start_pos = (0.0,0.0,0.0)
    weed = plant.Plant(start_pos)
    ''' run '''
    for i in range(steps):
        particle_system.move_particles()
        particle_system.re_spawn_escaped_particles()
        weed.collide_with(particle_system)
        box.resize_to_fit(weed.bbox_lower,weed.bbox_upper,padding=particle_system.radius*2.0)
    weed.show()
    box.show()
    '''Translate box and weed to edge of previous run'''
    from_vector = np.array((box.lower_vertex[0],0.0,0.0))
    move_vec = pos_vector - from_vector
    box.translate(move_vec)
    weed.translate(move_vec)
    pos_vector = move_vec + np.array((box.upper_vertex[0],0.0,0.0))

