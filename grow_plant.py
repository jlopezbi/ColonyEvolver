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

side = 10.0
height = 5.0 
front = (-side/2,-side/2,0.0)
back = (side/2,side/2,height)
box = world.BoxWorld(front,back)

num_particles = 60
particle_system = nutrients.ParticleSystem(num_particles,box)

start_pos = (0.0,0.0,0.0)
weed = plant.Plant(start_pos)

steps = 100
for i in range(steps):
    particle_system.move_particles()
    particle_system.re_spawn_escaped_particles()
    weed.grow_collided(particle_system.particles)

weed.show()
box.show()
particle_system.show_particles()
