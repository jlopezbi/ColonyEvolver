# [Coral Simulations and Evolution](https://jlopezbi.github.io/ColonyEvolver/)

generative growth algorithm inspired by plant and coral growth. Check out the blog [here](https://jlopezbi.github.io/ColonyEvolver/)


## How the Growth Simulation Works
Spherical particles jitter downwards. These are the 'nutrients' for the colony that grows.
A box contains the particles and the colony. If a particle goes outside the box, it is moved back to the top plane of the box. The colony is a collection of nodes, cNode for colony node. Each node has a location in 3d space, and stores a pointer to its parent node.  In each step of the simulation the particles move some small amount, and then all of the collisions between the particles and the colony nodes are computed. If a particle collides with some nodes, one of them is chosen (at this point it is arbitrary which one) to recieve the message that it was collided. The cNode can do whatever it likes with this information. It could spawn a child node, save the data, send a message to another cNode, etc. This is where things get creative!

## Current Goal
Of course it is possible to write a program for the colony nodes that decides what to do when the cNode gets a collision. I have played around a little with different cNode behaviors. But more interesting to me is evolving that program. At the moment a genetic programming (gp) approach is used to evolve the 'mini-program' that acts as the decision maker for the colony nodes.


## Images
![screen shot 2016-10-19 at 11 25 22 am](https://cloud.githubusercontent.com/assets/3253027/19532080/07b6a552-95ef-11e6-8d68-3091f46881ab.png)
Above: A plant-shape, or perhaps more like a coral-shape, that was grown using PlantGrower. In this case particles with a strong donward tendency and a new-node-position rule that computed the position P as follows. P is the the average vector C between two vectors A and B and added it to the node position. A is the vector from the collided-node to the particle center. B is the vector from the gradparent node to the current node.

![screen shot 2016-10-13 at 10 59 15 am](https://cloud.githubusercontent.com/assets/3253027/19360869/2951f144-9135-11e6-9f9d-b1107802b3a7.png)
The above is the first "plant" grown using this system. In this case new nodes were added to the plant each time a particle (sphere) collided with a pre-existing node, the 'parent' node. The new node's location was the center of the sphere.

## Developer Notes
run 'grip' to render this markdown file


