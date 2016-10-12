import unittest,imp
import nutrients,world
import numpy as np
imp.reload(nutrients)
imp.reload(world)

class ParticleSystemTestCase(unittest.TestCase):

    def setUp(self):
        self.box = world.BoxWorld((0.0,0.0,0.0),(5.0,10.0,5.0))
        self.n_particles = 100
        self.system =nutrients.ParticleSystem(self.n_particles,self.box)

    def test_intialize_particleSystem(self):
        self.system =nutrients.ParticleSystem(self.n_particles,self.box)

    def test_shows_particles(self):
        self.system.show_particles()
        self.box.show()

    def test_moves_particles(self):
        self.system.move_particles()
        self.system.show_particles()

    def test_re_spawns(self):
        system = nutrients.ParticleSystem(1,self.box)
        self.system.particles[0].set_position((100.0,100.0,100.0))
        self.system.show_particles()
        self.assertFalse(self.box.particle_is_inside(self.system.particles[0]))
        self.system.re_spawn_escaped_particles()
        self.assertTrue(self.box.particle_is_inside(self.system.particles[0]))




if __name__=="__main__":
    unittest.main(exit=False)
