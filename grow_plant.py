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

'''set up'''
side = 2.0
height = 3.0 
front = (-side/2,-side/2,0.0)
back = (side/2,side/2,height)
box = world.BoxWorld(front,back)

num_particles = 60
particle_system = nutrients.ParticleSystem(num_particles,box)
particle_system.randomness_of_motion = 0.1
particle_system.radius = .5
particle_system.trend_motion_magnitude = .1
padding_multiplier = 2.0

start_pos = (0.0,0.0,0.0)
second_pos = (0.0,0.0,0.5)
primitive_set = brain.make_vec_pset()
pBrain,expr = brain.make_processor_tree(primitive_set,minDepth=4,maxDepth=20)
brain.plot_processor_tree(expr)
first_node = nodes.RandomBrainNode(parent=None,location=start_pos,processor=pBrain)
second_node = nodes.RandomBrainNode(parent=first_node,location=second_pos,processor=pBrain)
#weed = plant.Plant(start_pos,nodes.RandomBrainNode)
weed = plant.Plant(first_node)
weed.append_node(second_node,old_node=first_node)

''' run '''
steps =60
for i in range(steps):
    particle_system.move_particles()
    particle_system.re_spawn_escaped_particles()
    weed.collide_with(particle_system)
    box.resize_to_fit(weed.bbox_lower,weed.bbox_upper,padding=particle_system.radius*padding_multiplier)

weed.show()
box.show()
#particle_system.show_particles()
