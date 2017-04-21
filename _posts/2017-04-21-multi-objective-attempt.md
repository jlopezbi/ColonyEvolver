---
layout: default
title:  "Multi Objective First Attempt"
date:   2017-04-21 
categories: main
---

*Here is my first succesful attempt to run a multi-objective evolution, documented using [jupyter](http://jupyter.org/). Many thanks to [this post](http://briancaffey.github.io/2016/03/14/ipynb-with-jekyll.html) explaining how to put a jupyter session into a jekyll blog. Summary of this post: multi-objective worked and spat out a range of solutions. The solutions are on a frontier that at first sight looks not-optimal, but may be so because of the problem formulation.*


```python
import evolve_colony_multi_obj as ev
```

The imported module is a script with a main() function that runs the evolution. The fitness evaluator outputs (size, health) for the evaluated phenotype (a colony of nodes).


```python
info = ev.main()
```

    /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/transforms3d/quaternions.py:400: RuntimeWarning: invalid value encountered in divide
      vector = vector / math.sqrt(np.dot(vector, vector))


       	      	                                                           fitness                                                           	              size             
       	      	-----------------------------------------------------------------------------------------------------------------------------	-------------------------------
    gen	nevals	avg                          	max                          	min                        	std                          	avg  	max	min	std    
    0  	25    	[ 179.69142857  100.03209854]	[ 439.57142857  355.        ]	[  2.         -19.99791905]	[ 158.46217436  167.08081721]	24.52	142	2  	31.9826
    1  	48    	[ 227.76571429   16.73458574]	[ 447.          364.64285714]	[  2.         -16.86966543]	[ 143.79577287  101.42524822]	27.2 	181	2  	40.9185
    2  	46    	[ 233.31428571   17.55206654]	[ 447.          364.64285714]	[  2.         -16.86966543]	[ 138.30070167  102.03801106]	33   	311	2  	65.8331
    3  	45    	[ 235.76571429   20.21989035]	[ 447.          364.64285714]	[  2.         -16.06184076]	[ 153.93481727  102.09670425]	52.6 	679	2  	138.627
    4  	39    	[ 175.50285714   38.46083977]	[ 448.57142857  364.64285714]	[  2.         -16.71785968]	[ 145.44557363  120.98575388]	147.32	682	2  	245.975
    5  	46    	[ 173.79428571   37.89007022]	[ 448.57142857  364.64285714]	[  2.         -16.71785968]	[ 137.98761897  121.15668099]	110.2 	682	2  	199.476
    6  	41    	[ 190.66285714   39.57204475]	[ 448.57142857  364.64285714]	[  2.         -16.71785968]	[ 147.25656566  121.45121315]	55.76 	680	2  	138.259
    7  	46    	[ 148.56         61.71167985]	[ 448.57142857  364.64285714]	[  2.         -16.71785968]	[ 152.06825492  134.6276333 ]	95.76 	680	2  	181.183
    8  	45    	[ 143.56571429   87.54939393]	[ 448.57142857  364.64285714]	[  2.         -16.71785968]	[ 154.78536808  156.97171347]	130.36	680	2  	215.877
    9  	47    	[ 173.69714286   21.5299556 ]	[ 448.57142857  367.85714286]	[  2.         -16.71785968]	[ 157.46930933   77.42182592]	123.8 	680	2  	183.769
    10 	46    	[ 160.92571429   27.50332923]	[ 448.57142857  367.85714286]	[  2.         -16.71785968]	[ 159.32660395   79.07821019]	120.28	680	2  	147.794



```python
n_nodes = []
health = []
for individual in info.final_pop:
    N,H = individual.fitness.values
    n_nodes.append(N)
    health.append(H)
```


```python
import matplotlib.pyplot as plt
```


```python
plt.scatter(n_nodes, health)
plt.xlabel("Number of Nodes")
plt.ylabel("Colony Health")
plt.show()
```


![png]({{ site.url }}{{ site.baseurl }}/assets/multi-objective-first-plot.png)


Well at first glance this is completely the reverse of what I was hoping to see.
#### Hypothesis 1: 
It looks as if the ea is trying to minimize the number of nodes and the colony health. This is not what the code specifies.
#### Hypothesis 2: 
I did set up a system where high health is likely to be achived by a colony with a low number of nodes, and vice-versa. It could be that this curve, which looks like an inverse-relationship, is a result of the mechanics of the system. It might be inevitable. If that is the case I would expect to see the curve bump out generation by generation.


```python
import numpy as np
np.flip(np.argsort(health), 0)
```
    array([ 3,  4, 17, 14, 23, 22, 21, 20, 24, 19, 16, 15,  8, 12, 10,  9,  7,
           18, 11,  5,  6, 13,  2,  1,  0])
```python
idx = 10
genome = info.final_pop[idx]
p = ev.make_phenotype(genome)
```
```python
p.number_of_elements()
```
    165
```python
p.get_health()
```
    -11.16969696969697
```python
print(genome)
```
    cross(unit_vector(unit_vector(if_greater_vec(0.25020023985559803, -0.7933540587822074, mean_vec(unit_vector(rotate_vec(x, y, c1)), if_greater_vec(dot(x, y), if_greater_float(1.1726666718815764, 3.989947694119547, 5.2722279587631125, 0.03282991090630774), cross(x, x), rotate_vec(x, y, -0.5499783240629201))), x))), x)

```python
p.show()
```

Below is a screen shot of the 3d view generated by show():
![img]({{ site.url }}{{ site.baseurl }}/assets/crazy_zigzag.png)
It makes sense that this has low health! The nodes below are being starved for nutrients. But it has many nodes. After inspecting alot of the solutions, I think the evolution may be working right after all (looks like Hypothesis 2 is pulling ahead). Next steps are to make a compiliation of the images for all of the solutions in this final population.

As a teaser, here is another one
from idx = 24:
![img]({{ site.url }}{{ site.baseurl }}/assets/baby_cone.png)
(number of nodes = 24, health = 19 )
