import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/')
#TODO: if want other people to use this figure out how to get them this dependency!
import deap.gp as gp
import pygraphviz as pgv
import numpy as np
import vector_operations
import math, random
import uuid


'''
inputs:(collision event) rel_sphere_pos, rel_parent_pos
constants: ? maybe a constant vector like z up?
output: new_node_position 
'''

def scale_protected(array,scalar): 
    if scalar == 0.0:
        return array
    return array*scalar

def subtractnz(array_x,array_y): return array_x if (array_x==array_y).all() else array_x-array_y

def mean_vec(x,y):
    c = np.column_stack([x,y])
    return np.mean(c,axis=1)

def add_scalar(x,y):
    return x+y

def mult_scalar(x,y):
    return x*y

def if_greater_vec(w,x,y,z):
    return if_greater(w,x,y,z)

def if_greater_float(w,x,y,z):
    return if_greater(w,x,y,z)

def if_greater(w,x,y,z):
    '''
    w float
    x float
    y any type
    z any type
    '''
    return if_else(greater(w,x),y,z)

def greater(x,y):
    return x >= y

def if_else(x,y,z):
    return y if x else z

def larger(): pass

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    if not vector.any():
        return vector
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    return np.cross(x,y)

def x_comp(v):
    return v[0]

def y_comp(v):
    return v[1]

def z_comp(v):
    return v[2]

def big_pset():
    vec = np.ndarray
    two_in = [vec ,vec ]
    pset = gp.PrimitiveSetTyped("main",two_in,vec )
    ''' vec '''
    pset.addPrimitive(np.dot,two_in,float)
    pset.addPrimitive(np.cross,two_in,vec)
    pset.addPrimitive(mean_vec,two_in,vec )
    pset.addPrimitive(vector_operations.rotate_vec_np,[vec ,vec ,float],vec )
    pset.addPrimitive(scale,[vec ,float],vec )
    pset.addPrimitive(np.linalg.norm, [vec ],float)
    pset.addPrimitive(angle_between,[vec ,vec ],float)
    pset.addPrimitive(unit_vector,[vec],vec)
    pset.addPrimitive(if_greater_vec, [float,float,vec ,vec], vec)
    pset.addPrimitive(x_comp, [vec],float)
    pset.addPrimitive(y_comp, [vec],float)
    pset.addPrimitive(z_comp, [vec],float)
    '''non vec'''
    pset.addPrimitive(add_scalar, [float,float], float)
    pset.addPrimitive(if_greater_float, [float, float, float, float ], float)
    pset.addPrimitive(mult_scalar, [float, float], float)
    pset.addTerminal(.5,float,'c1')
    pset.addEphemeralConstant(str(uuid.uuid1()),lambda: random.uniform(0, math.pi*2.),float)
    pset.addEphemeralConstant(str(uuid.uuid1()),lambda: random.uniform(-1,1),float)
    pset.renameArguments(ARG0="x")
    pset.renameArguments(ARG1="y")
    return pset

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
    pset.addTerminal(.5,float,'c1')
    e_name = str(uuid.uuid1())
    #pset.addEphemeralConstant(e_name,lambda: random.uniform(0, math.pi*2.),float)
    #pset.addEphemeralConstant(str(uuid.uuid1()),lambda: random.uniform(0,1),float)
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
        l = labels[i]
        if type(l) == float:
            l = round(l,2)
        n.attr["label"] = l
    g.draw("cat.pdf")

def generate_processor_tree(pset,minDepth,maxDepth):
    '''
    generates a function that is composed of randomly selected primitives
    '''
    expr = gp.genGrow(pset,min_=minDepth,max_=maxDepth)
    tree = gp.PrimitiveTree(expr)
    return tree,gp.compile(tree,pset)

defualt_filename = 'tree.txt'

def load_text(filename):
    f = open(filename,'r')
    return f.read()

def save_processor_tree(tree,filename=defualt_filename):
    '''
    saves string representaiton of the processor tree
    as a text file
    '''
    with open(filename, "w") as text_file:
        print(str(tree), file=text_file)

def resurrect_processor_tree(pset,tree_string=load_text(defualt_filename)):
    tree = gp.PrimitiveTree.from_string(tree_string,pset)
    return tree,gp.compile(tree,pset)


if __name__=="__main__":
    pset = big_pset()
    expr = gp.genGrow(pset,min_=3,max_=3)
    tree = gp.PrimitiveTree(expr)
    processor = gp.compile(tree,pset)
    print(tree)
    x = np.array((1.1,0.3,0.2))
    y = np.array((2.0,1.9,1.5))
    print(processor(x,y))
    plot_processor_tree(expr)


