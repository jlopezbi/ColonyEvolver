---
layout: default
title: "my snap-personification of an evolutionary algorithm"
categories: main
---

A funny thing happened a few weeks ago. I was getting an evolution running with a fitness criteria that rewarded individual colonies for having a number of nodes close to a target number (T). I set T=13, arbitrarily.
I was using this simple fitness criteria because I wanted to ensure that evolutions were getting better, and also see if different evolution runs resulted in a variety of structures.
So I ran an evolution search for 13 node colonies, and I got structures where all but the seed nodes had location=(NaN, NaN, NaN).
Of course this resulted in no appreciable strcture, so it was not visually interesting to look at. This happened because of a loop-hole in the primitive functions I had supplied to the genetic-programming framework. So I made sure no NaN values could be produced. Next run of the evolution a similar thing happened but with all zeros (location = (0, 0, 0) ).
At this point I thought to myself "whoa it is taking advantage of the system!" Without realizing I was treating the algorithm as if it had intention, as if it were a deceptive trickster. Well, certainly I had explicitly set the intention to 13 node-colonies. But I felt I was battling, or perhaps collaborating, or conversing with this entity that had intention of its own. I guess it preferred simpler solutions, all NaN's or all zeros; more nothingness, less shape.
Whereas I wanted shape, something to look at.
Funny how quickly I seemed willing to prescribe an "intelligent" actor even though I had set up the mechanism in the first place!



