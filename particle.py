import bpy
import numpy as np
import random,math
#NOTE: working here to set up particles system

class ParticleSystem(object):
    """ This type of Nutrients is composed of particles """

    def __init__(self,num_particles,world):
        self.grav_factor = .5
        self.radius = .6
        self.num_particles = num_particles
        self.particles = []
        self._init_particles(self,world)

    def _init_particles(self,world):
        for i in range(num_particles):
            position = world.get_random_pos_on_top()
            self.particles.append(Particle(position,self.radius,self.grav_factor))

    def show_particles(self):
        for p in self.particles:
            p.show()


class Particle(object):

    def __init__(self,position,radius,grav_factor):
        self.position = np.array(position)
        self.radius = radius
        self.peak_inclination = math.pi*grav_factor

    def move(self,speed):
        displacement_vec = self._get_displacement_vector(speed)
        self.position += displacement_vec

    def show(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        #bpy.ops.object.empty_add(type='SPHERE',radius=self.radius,location=(x,y,z))
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=self.radius,location=(x,y,z))

    def _get_displacement_vector(self,speed):
        inclination = random.triangular(0,math.pi+.00001,self.peak_inclination)
        azimuth = random.uniform(0,math.pi*2.0)
        velX = speed*math.sin(azimuth)*math.cos(inclination)
        velY = speed*math.sin(azimuth)*math.sin(inclination)
        velZ = speed*math.cos(inclination)
        return np.array([velX,velY,velZ])

'''
time_steps = 1000
p1 = Particle(np.array([0.0,1.0,1.0]),1.0,.5)
for i in range(time_steps):
    p1.move(1.7)
    p1.draw()
'''
