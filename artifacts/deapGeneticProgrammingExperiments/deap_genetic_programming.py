import deap.gp as gp
import numpy as np



array_type = np.ndarray
unit_x = np.array((1.0,0.0,0.0))
p = 1.0
pset = gp.PrimitiveSetTyped("main",[array_type,array_type],array_type)
pset.addPrimitive(np.add,[array_type,array_type],array_type)
pset.addPrimitive(np.subtract,[array_type,array_type],array_type)
pset.addPrimitive(np.multiply,[array_type,array_type],array_type)
#pset.addPrimitive(np.divide,2)
#pset.addPrimitive(np.maximum,2)
#pset.addPrimitive(np.minimum,2)
#pset.addPrimitive(np.reciprocal,1)
pset.addTerminal(unit_x,array_type,"unit_x")
pset.renameArguments(ARG0="x")
pset.renameArguments(ARG1="y")

expr = gp.genFull(pset,min_=1,max_=6)
tree = gp.PrimitiveTree(expr)
print(tree)
 
function = gp.compile(tree,pset)
x = np.array((1.0,1.0,0.0))
y = np.array((2.0,1.0,1.5))

print(function(x,y))
