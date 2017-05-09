---
layout: default
categories: main
---
[//]: # What is this project?
[//]: # Exploration of Generative Growth, Evolution.

# Why Am I Doing this?
This project is for fun, curiosity and art. It satisfies that part that enjoys programing and science.

Here are some things that are driving this project:

* Aesthetic Hypothesis: **Intruiging forms arise in growth systems that are forced to contend with the interaction of competing forces.**
* Love of sessile organisms
* Interest in Evolution
* Curious about selfish/altruistic dichotomy in life
* Curious about computer programs that are creative and surprise me


# How the Simulation Works
Spherical particles jitter around in a box. They move in a random 3d-walk, biased donwards. The biased random walk simulates diffusing particles in water, slighly effected by gravity. These are the 'nutrients' for the colony that grows. If a particle goes outside the box, it is moved back to the top plane of the box. 

A 'seed' colony is placed in the box.  The seed colony is some intial collection of nodes, cNode for colony node. Each cNode has a location in 3d space, and stores a pointer to its parent node. This is naturally visualized as a line segment connecting the two cNodes. In each step of the simulation the particles move some small amount, and then all of the collisions between the particles and the colony nodes are computed. If a particle collides with some cNodes, one of them is chosen (at this point it is arbitrary which one) to recieve the message that it was collided. The cNode just 'ate!' It can do whatever it likes with this information. It can spawn a child node, save the data, send a message to another cNode, etc. This is where things get creative!

A bunch of other posts about this project are here: [joshlopezbinder.com](http://joshlopezbinder.com/)

[//]: # How the Evolution Works



