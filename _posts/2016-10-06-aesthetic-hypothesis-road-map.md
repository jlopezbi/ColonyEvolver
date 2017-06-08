---
layout: post
title: "An Aesthetic Hypothesis and a Road-Map" 
date: 2016-10-06
categories: main
---
# Aesthetic Hypothesis

When I look at natural systems like a tree, a cat, a city, a grassy field, I imagine that all that harmony actually comes from relationships full of tension and struggle. Of course the connotations associated with tension and struggle tend to be negative, but in the non-designed systems they are the ingredients of balance and peace. (see end-note 1)

I have an aesthetic hypothesis: **Intruiging forms arise from the interaction of competing forces.**

For example, according to the hypothesis, the tree is beautiful in part because there is tension between the impetus to grow taller and bigger, and the need to exchange liquid, sugars, and nutrients between the foliage and the roots. Of course many more factors influence a tree's development, but these are a few simplified examples that I may try to encode into a simulated creature.

I intend for this project to be an exploration of a few things:
* Tension and the search for balance in natural systems
* The beautiful and complex shapes produced by various sessile (non-moving) organisms.
	- sponges
	- corals
	- plants
* What might happend when I create strange or unfamiliar situations. 

# Project Lineage
This project is an offshoot of the meshDLA or [Coral Simulation project](http://golancourses.net/2013/projects/study-for-biomimetic-heat-sinks-coral-growth/) I did in college in Golan Levin's class centered on programing and art/design.

In that project I created a simulation system where a mesh "grew" according to rules based on biological stony corals. The simulation worked like this: a set of spheres moved in a pseudo random walk, biased down. When any particle intersected a node of the mesh (the "coral") that node moved outward along the vertex normal, thus "growing". The result were vaguely branched, coral-like forms. The ideas for this simulation were simplified versions of methods described in this book: [The Algorithmic Beauty of Seaweeds, Sponges and Corals](http://www.springer.com/us/book/9783540677000).

The most interesting part of the experience was exploring the range of possible forms afforded by the simulation system. What would happen if the particle size was relatively much bigger than the mesh-edge size? Or what would happen after a very long run of the simulation? I hardly explored these questions because at the time the project was mostly about getting the damn thing to work, and then printing the shape. At the time I also thought the project might be useful for generating heat-sink forms, but since then I feel it is more about exploring growth systems and form.

I also realized that, in the abstract, the project consisted of an environment wich contains a nutrient or energy source, and a structure which interacts with this environment. These ideas were clarified and vocabulary was added by the this paper: [Visual Models of Plants interacting with Their Environment][1]. Even more abstract: an environment that provides information to a structure, which in turn affects the environment.
This abstraction opened up a whole new set of possible growth behaviors: Stick-like bushes that grow up into the particle-cloud, nutrients that behave like rays of light, shifting across the sky, dual nutrients, which move in different ways.
The hope, then, is to explore more than to engineer.

# A Proposed Road-Map
# Exploration of interesting shapes [B]:
* investigate already-existing frameworks and libraries that could make this project less about the engineering, more about the exploration
	* figure out what sort of function calls/behavior will make it easy to build
		* pseudo-code
		* exploring current meshDLA code 

DECISION: Blender

TODO:
- figure out workflow
- play around with particle sim
* Set up simulation framework
* create various nutrient/creature modules and observrve the result of their interaction

# Exploration of tension [A]:
* find ways to codify creature growth rules to put into a evolutionary algorithm; set up cost-functions combine factors that are at-odds with each other

Structures:
* node-edge skeletons
* meshes
* surfaces like sails
* flexible strings

Nutrients:
* particles
* rays
* sheets



[1]: http://algorithmicbotany.org/papers/enviro.sig96.pdf 

### End Notes (2017-05-09)
(1) Since writing this I read the [Selfish Gene](https://en.wikipedia.org/wiki/The_Selfish_Gene) and a few chapeter of the [Extended Phenotype](https://en.wikipedia.org/wiki/The_Extended_Phenotype). This has much clarified my notions of harmony and discord in the context of organisms.



