import bpy
import sys,os,imp
loc = os.path.dirname(bpy.data.filepath)
if not loc in sys.path:
    sys.path.append(loc)

import crumbs
import world
imp.reload(crumbs)
imp.reload(world)

box = world.BoxWorld((0.0,0.0,0.0),(5.0,10.0,5.0))












init_pos = (2.5,2.5,2.5)
p = particle.Particle(init_pos,0.1,.8)
print("Particle is in box:{}".format(box.particle_is_inside(p)))
p.show()
box.show()
steps = 100
speed = 0.1
for i in range(steps):
    print("step {}".format(i))
    p.move(speed)
    p.show()
    if not box.particle_is_inside(p):
        print("particle hit wall!")
        break
