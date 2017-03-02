import unittest,imp,random
import nutrients
import numpy as np
imp.reload(nutrients)


class ParticleNutrientsTestCase(unittest.TestCase):
    def setUp(self):
        pos = (0.0,0.0,0.0)
        radius = .7
        trend_velocity = (0.0,0.0,-1.0)
        self.p = nutrients.Particle(pos,radius)

    def test_move(self):
        original_position = np.array(self.p.position)
        self.p.move(magnitude=1.0)
        moved_position = np.array(self.p.position)
        self.assertFalse(np.array_equal(original_position,moved_position))

    def test_shows(self):
        self.p.show()

    def test_get_random_vector(self):
        test_number = random.uniform(0.0,2000.)
        vec = self.p._get_random_vector(magnitude=test_number)
        self.assertAlmostEqual(np.linalg.norm(vec),test_number,places=10)

if __name__=="__main__":
    unittest.main(exit=False)



