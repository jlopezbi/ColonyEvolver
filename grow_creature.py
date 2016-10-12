import world
import ParticleNurients
import plant

nutrients = particles.ParticleSystem()
creature = plant.Branchy()
bounds = world.BoxWorld()


for i in range(time_steps):
    nutrients.interact_with_creature(bounds,creature)
    creature.grow_according_to_nutrients(nutrients)
    bounds.resize(creature)

