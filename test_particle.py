import unittest,imp
import nutrients
import numpy as np
imp.reload(nutrients)


class ParticleTestCase(unittest.TestCase):
    def setUp(self):
        pos = (0.0,0.0,0.0)
        radius = .7
        trend_velocity = (0.0,0.0,-1.0)
        self.p = nutrients.Particle(pos,radius,trend_velocity)

    def test_move(self):
        original_position = np.array(self.p.position)
        self.p.move()
        moved_position = np.array(self.p.position)
        self.assertFalse(np.array_equal(original_position,moved_position))

    def test_shows(self):
        self.p.show()

if __name__=="__main__":
    unittest.main(exit=False)



