import unittest,imp
import mathutils
import plant
imp.reload(plant)

class StubbedParticle(object):
    def __init__(self,location=(0.0,0.0,0.0),radius=2.0):
        self.position = mathutils.Vector(location)
        self.radius = radius

class PlantTestCase(unittest.TestCase):
    def setUp(self):
        self.plant = plant.Plant((0.0,0.0,0.0))

    def test_show(self):
        self.plant.show()

    def test_grow_collided(self):
        N = 2
        particles = [StubbedParticle() for i in range(N)]
        particles = [StubbedParticle((0,0,1),3)]
        self.plant.grow_collided(particles)
        self.assertTrue(self.plant.number_of_elements(),2)
        self.plant.show()


if __name__=="__main__":
    unittest.main(exit=False)
