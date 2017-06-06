import numpy as np
import random
import math
# NOTE: working here to set up particles system


class ParticleSystem(object):
    ''' composed of world an a set of particles.
    perhaps this is the main simulation
    '''

    def __init__(self, world):
        self.world = world
        self.randomness_of_motion = 0.0  # [0, 1.0]
        #NOTE: probs should make magnitude of trend motion some multiple of particle radius
        self.trend_speed = 0.3
        self.trend_direction = np.array((0.0,0.0,-1.0))
        self.radius = .6
        self.particles = []
        #self.set_initial_positions()
        #self.add_n_particles_at_spawn_loc(self.num_particles)
        self.n_particles_per_area = None
        self.MAX_PARTICLES= 80

    def finalize(self):
        '''
        allows setting parameters and then 'baking' them into the class
        '''
        self.n_particles_per_area = self.get_n_particles_per_area(self.radius)

    def get_particle(self, idx):
        return self.particles[idx]

    def get_matrix_form(self):
        return np.stack(self.get_particle_vectors(), axis=0)

    def get_particle_vectors(self):
        return [particle.position for particle in self.particles]

    def add_n_particles_at_spawn_loc(self, n=None, radius=None):
        if radius == None:
            radius = self.radius
        for i in range(n):
            position = self.world.get_a_spawn_location()
            self.particles.append( Particle(position, radius) )

    def num_particles(self):
        return len(self.particles)

    def set_initial_positions(self):
        #perhaps adding all the particles to the top plane and the running
        #the simulation causes some odd stuff to happen right at the beginning
        # i.e. a ton of particles colliding in a small time frame. How to space it out?
        for i in range(self.num_particles()):
            position = self.world.get_a_spawn_location()
            self.particles.append(Particle(position, self.radius ))

    def show_particles(self):
        for p in self.particles:
            p.show()

    def move_particles(self):
        '''
        sends command to all particles to
        move
        '''
        for p in self.particles:
            p.move(self.randomness_of_motion)

    def add_missing_particles_if_required(self):
        area = self.world.get_footprint_area()
        num_missing = self.calculate_missing_particles_per_area(area)
        if num_missing > 0 and self.num_particles() < self.MAX_PARTICLES:
            self.add_n_particles_at_spawn_loc( num_missing )
        #FOR NOW: colonies cannot get smaller, so there is no need to worry about
        # removing particles
        #More than MAX_PARTICLES could result in very slow computation (or memory, something like that)

    def calculate_missing_particles_per_area(self, area):
        ideal_n = math.trunc(area * self.n_particles_per_area)
        missing = ideal_n - self.num_particles()
        return missing

    def get_n_particles_per_area(self,radius):
        '''
        This is basically saying "pretend the particles are cubes,
        so that the # of particles is determined by how many cubes can
        fit in an area."
        1 particle for every (radius^2) area
        '''
        return 1.0 / radius**2

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

    def re_spawn_particle(self,particle):
        '''
        moves particle back to spawn location
        '''
        new_pos = self.world.get_a_spawn_location()
        particle.set_position(new_pos)


    def show_case_particle_motion(self,steps=10):
        init_pos = (0.,0.,0.)
        p1 = Particle(init_pos,self.radius)
        for i in range(steps):
            p1.move(self.trend_speed,self.trend_direction,self.randomness_of_motion)
            p1.show()

class Particle(object):

    def __init__(self, position, radius ):
        self.position = np.array(position)
        self.radius = radius
    
    def set_position(self,new_position):
        self.position = np.array(new_position)

    def move(self,magnitude,trend_direction=(0.0,0.0,-1.0), randomness=0.5):
        '''
        randomness is in range [0,1] for random brownian-like motion
        '''
        trend_velocity = np.array(trend_direction)*magnitude
        displacement_vec = trend_velocity*(1.-randomness) + self._get_random_vector(magnitude)*randomness
        self.position += displacement_vec


    def show(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        #print("show not implemented yet")
        pass

    def _get_random_vector_biased(self, speed):
        '''
        depricated function using traingular distribution to
        bias movement
        '''
        self.peak_inclination = math.pi * grav_factor
        inclination = random.triangular(
            0, math.pi + .00001, self.peak_inclination)
        azimuth = random.uniform(0, math.pi * 2.0)
        velX = speed * math.sin(azimuth) * math.cos(inclination)
        velY = speed * math.sin(azimuth) * math.sin(inclination)
        velZ = speed * math.cos(inclination)
        return np.array([velX, velY, velZ])
    
    def _get_random_vector(self,magnitude=1.0):
        '''
        get a randomly oriented vector with input magnitue
        '''
        inclination = random.uniform(0, math.pi)
        azimuth = random.uniform(0, math.pi * 2.0)
        X = magnitude * math.sin(azimuth) * math.cos(inclination)
        Y = magnitude * math.sin(azimuth) * math.sin(inclination)
        #Z = magnitude * math.cos(inclination)
        Z = magnitude * math.cos(azimuth)
        return np.array([X, Y, Z])

