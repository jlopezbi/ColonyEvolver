#Plant Simulations in Blender
generative growth algorithm inspired by plant growth
Currently in development.

## To Run
- download blender: www.blender.org
- in blender open the template.blend file included in this repository
- change blender to script viewport mode
- load the grow_plant.py script from this repository and press "run"

## First Iteration Strategy
particles jitter downwards.
A box world contains particles. If a particles goes outside the boz, it is moved back to the top plane of the box.
A directed graph structure grows new nodes each time a particle collides with a node.

## Images
![screen shot 2016-10-19 at 11 25 22 am](https://cloud.githubusercontent.com/assets/3253027/19532080/07b6a552-95ef-11e6-8d68-3091f46881ab.png)
Above: A plant-shape, or perhaps more like a coral-shape, that was grown using PlantGrower. In this case particles with a strong donward tendency and a new-node-position rule that computed the position P as follows. P is the the average vector C between two vectors A and B and added it to the node position. A is the vector from the collided-node to the particle center. B is the vector from the gradparent node to the current node.

![screen shot 2016-10-13 at 10 59 15 am](https://cloud.githubusercontent.com/assets/3253027/19360869/2951f144-9135-11e6-9f9d-b1107802b3a7.png)
The above is the first "plant" grown using this system. In this case new nodes were added to the plant each time a particle (sphere) collided with a pre-existing node, the 'parent' node. The new node's location was the center of the sphere.

