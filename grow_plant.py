import sys,os,imp
import bpy
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)

import plant
import nutrients
import world
imp.reload(plant)
imp.reload(nutrients)
imp.reload(world)

'''set up'''
side = 2.0
height = 3.0 
front = (-side/2,-side/2,0.0)
back = (side/2,side/2,height)
box = world.BoxWorld(front,back)

num_particles = 90
particle_system = nutrients.ParticleSystem(num_particles,box)
particle_system.randomness_of_motion = 0.5
particle_system.radius = 1.2
particle_system.trend_motion_magnitude = .6

start_pos = (0.0,0.0,0.0)
weed = plant.Plant(start_pos)

''' run '''
steps = 3000
for i in range(steps):
    particle_system.move_particles()
    particle_system.re_spawn_escaped_particles()
    weed.collide_with(particle_system)
    box.resize_to_fit(weed.bbox_lower,weed.bbox_upper,padding=particle_system.radius*.7)

weed.show()
box.show()
#particle_system.show_particles()
