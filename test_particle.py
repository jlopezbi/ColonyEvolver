import unittest,imp
import nutrients
import numpy as np
imp.reload(nutrients)


class ParticleTestCase(unittest.TestCase):
    def setUp(self):
        pos = (1.0,1.0,1.0)
        radius = .7
        grav_factor = 1.0
        self.p = nutrients.Particle(pos,radius,grav_factor)

    def test_move(self):
        speed = 1.0
        self.p.move(speed)

    def test_shows(self):
        self.p.show()

if __name__=="__main__":
    unittest.main(exit=False)



