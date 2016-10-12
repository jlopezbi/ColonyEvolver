#Plant Simulations in Blender
generative growth algorithm inspired by plant growth
Currently in development.

## To Run
- download blender: www.blender.org
- change blender to script viewport mode
- load a script from this repository and press "run"

## First Iteration Strategy
particles jitter downwards.
A box world contains particles. If a particles goes outside the boz, it is moved back to the top plane of the box.
A directed graph structure grows new nodes each time a particle collides with a node.


