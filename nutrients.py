import bpy
import numpy as np
import random
import math
# NOTE: working here to set up particles system


class ParticleSystem(object):
    ''' composed of world an a set of particles.
    perhaps this is the main simulation
    '''

    def __init__(self, num_particles, world):
        self.world = world
        self.speed = 1.0 #function of world length scale?
        self.grav_factor = 1.0
        self.radius = .6
        self.num_particles = num_particles
        self.particles = []
        self._init_particles()

    def _init_particles(self):
        for i in range(self.num_particles):
            position = self.world.get_a_spawn_location()
            self.particles.append(
                Particle(position, self.radius, self.grav_factor))

    def show_particles(self):
        for p in self.particles:
            p.show()

    def move_particles(self):
        '''
        sends command to all particles to
        move
        '''
        for p in self.particles:
            p.move(self.speed)

    def re_spawn_escaped_particles(self):
        #NOTE: working here, just need to try out running alot of particles
        #This is trivial solution. if it ends up being slow consider seraching for some sort of spatial data structure to solve problem
        '''
        particles that have escaped the world are moved back to spawn_plane
        '''
        for p in self.particles:
            if not self.world.particle_is_inside(p):
                new_pos = self.world.get_a_spawn_location()
                p.set_position(new_pos)


class Particle(object):

    def __init__(self, position, radius, grav_factor):
        self.position = np.array(position)
        self.radius = radius
        self.peak_inclination = math.pi * grav_factor
    
    def set_position(self,new_position):
        self.position = np.array(new_position)


    def move(self, speed):
        displacement_vec = self._get_displacement_vector(speed)
        self.position += displacement_vec

    def show(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        # bpy.ops.object.empty_add(type='SPHERE',radius=self.radius,location=(x,y,z))
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(
            radius=self.radius, location=(x, y, z))

    def _get_displacement_vector(self, speed):
        inclination = random.triangular(
            0, math.pi + .00001, self.peak_inclination)
        azimuth = random.uniform(0, math.pi * 2.0)
        velX = speed * math.sin(azimuth) * math.cos(inclination)
        velY = speed * math.sin(azimuth) * math.sin(inclination)
        velZ = speed * math.cos(inclination)
        return np.array([velX, velY, velZ])

'''
time_steps = 1000
p1 = Particle(np.array([0.0,1.0,1.0]),1.0,.5)
for i in range(time_steps):
    p1.move(1.7)
    p1.draw()
'''

