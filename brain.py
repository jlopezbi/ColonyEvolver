import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/')
#TODO: if want other people to use this figure out how to get them this dependency!
import deap.gp as gp
import pygraphviz as pgv
import numpy as np
import vector_operations
import math, random
import uuid

#TODO: work here to turn this into a module that nodes can import!

'''
inputs:(collision event) rel_sphere_pos, rel_parent_pos
constants: ? maybe a constant vector like z up?
output: new_node_position 
'''

def scale(array,scalar): return array*scalar

def subtractnz(array_x,array_y): return array_x if (array_x==array_y).all() else array_x-array_y

def mean_vec(x,y):
    c = np.column_stack([x,y])
    return np.mean(c,axis=1)


def larger(): pass

def make_vec_pset():
    '''
    primite set designed to take in vectors and scalars 
    '''
    array_type = np.ndarray
    #unit_x = np.array((1.0,0.0,0.0))
    two_in = [array_type,array_type]
    one_out = array_type
    pset = gp.PrimitiveSetTyped("main",two_in,array_type)
    #pset.addPrimitive(np.add,two_in,array_type)
    #pset.addPrimitive(subtractnz,two_in,array_type)
    #pset.addPrimitive(np.multiply,two_in,array_type)
    pset.addPrimitive(np.dot,two_in,float)
    #pset.addPrimitive(np.maximum,two_in,array_type)
    #pset.addPrimitive(np.minimum,two_in,array_type)
    pset.addPrimitive(mean_vec,two_in,array_type)
    pset.addPrimitive(vector_operations.rotate_vec_np,[array_type,array_type,float],array_type)
    pset.addPrimitive(scale,[array_type,float],array_type)
    pset.addPrimitive(np.linalg.norm, [array_type],float)

    
    #pset.addPrimitive(np.divide,two_in,array_type) gets divide by zero errors
    #pset.addPrimitive(np.reciprocal,two_in,array_type) gets divide by zero errors
    #pset.addTerminal(unit_x,array_type,"unit_x")
    #pset.addTerminal(.5,float,'c1')
    e_name = str(uuid.uuid1())
    pset.addEphemeralConstant(e_name,lambda: random.uniform(0, math.pi*2.),float)
    pset.addEphemeralConstant(str(uuid.uuid1()),lambda: random.uniform(0,1),float)
    pset.renameArguments(ARG0="x")
    pset.renameArguments(ARG1="y")
    return pset
'''
expr = gp.genFull(pset,min_=2,max_=10)
tree = gp.PrimitiveTree(expr)
print(tree)
 
function = gp.compile(tree,pset)
x = np.array((1.1,0.3,0.2))
y = np.array((2.0,1.9,1.5))
print(function(x,y))
'''

def plot_processor_tree(expression):
    '''
    creates a pdf image of the processor tree
    defined by expression
    '''
    nodes,edges,labels = gp.graph(expression)
    g = pgv.AGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="dot")
    for i in nodes:
        n = g.get_node(i)
        n.attr["label"] = labels[i]
    g.draw("cat.pdf")


def make_processor_tree(pset,minDepth,maxDepth):
    '''
    input: 
        pset of type  gp.PrimitiveSetTyped
        minDepth minimum depth of the processor tree
        maxDepth maxmium depth of the processor tree
    output:
        returns an executable function. Argument length and types are 
        deterimned by pset definition
    '''
    expr = gp.genGrow(pset,min_=minDepth,max_=maxDepth)
    tree = gp.PrimitiveTree(expr)
    return gp.compile(tree,pset),expr

if __name__=="__main__":
    pset = make_vec_pset()
    expr = gp.genGrow(pset,min_=0,max_=10)
    tree = gp.PrimitiveTree(expr)
    processor = gp.compile(tree,pset)
    x = np.array((1.1,0.3,0.2))
    y = np.array((2.0,1.9,1.5))
    print(processor(x))
    plot_processor_tree(expr)


