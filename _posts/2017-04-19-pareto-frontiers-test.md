---
layout: default
title:  "Multi Objective Evolution"
date:   2017-04-19 
categories: main
---

Today I spent some time understanding the [knapsack example](http://deap.readthedocs.io/en/master/examples/ga_knapsack.html?highlight=pareto), provided by the deap documentation. This is a great example for me because it uses multi-objective optimization, which is critical for my current curiosity. More on that in a future post.

For now, I needed to make sure that my understanding of multi-objective optimization corresponds with what is actually possible with DEAP. Since I like visuals, I decided to make a plot of what the evolution is doing. Here it is: 
![knapsack_img]({{ site.url }}{{ site.baseurl }}/assets/knapsack_populations.png)

Oooh pretty colors. This plot was made using [matplotlib](https://matplotlib.org/). The color map is matplotlib.cm.viridis.

Each color represents a population in the evolution. Brighter colors are newer populations. Each dot is an individual solution to the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem). In this case a randomly generated set, S, of (weight, value) items was generated. Each individual is a subset of S. The idea is to find individuals that have low weight, and high value. This is like the challenge a backpacker faces when trying to decide what items to put in her 'knapsack'. 
The tricky part of this problem for an evolutionary algorithm (ea) is that there are two ways to measure 'fitness': the total weight of the chosen items (which must be below 50 in this case) and the total value of the items. The easy way to adapt this to a normal ea is to perform a weighted sum of the two objectives. The problem is that by scaling the two metrics and suming, a bias is injected into the search. Only solutions that perform well for a particular level of relative importance between the objectives will be found. This is quite limiting when you are interested in seeing a wide range of good solutions. Other problems exist with the weighted sum approach: How does one scale objectives that have unkown bounds? How does one scale objectives that have radically different meanings or units?

Luckily there is an elegant way to completely avoid cobbling disimilar metrics together. The essential idea is the [pareto frontier](https://en.wikipedia.org/wiki/Pareto_efficiency). Basically this is the set of all individuals that are the best in their own special way (this property is called 'non-dominated'). All the evolution has to do is select individuals from the pareto frontier, and after many generations the frontier gets better and better. See the wikipedia on [multi-objective optimization](https://en.wikipedia.org/wiki/Multi-objective_optimization).

So if we plot the weight and value for each individual, and color them by generation, we should see the dots forming a sort of buldge that moves further from the previous colors. This is indeed what we see. I was a little confused at first that the bulge moved to the upper right. This is reconciled by the fact that the algorithm is selecting for low weight. 

Also, wow matplotlib's new default plotting looks pretty good. Go open source!!


