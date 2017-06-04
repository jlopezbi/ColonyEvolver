
'''
Initialized on 2016/12/16
Josh Lopez-Binder. hi!
copied from
https://github.com/DEAP/deap/blob/a90d3d599aa789a0083f5bc299803ec32d491cbd/examples/gp/symbreg.py
'''

from __future__ import print_function
import sys, imp
import deap.gp as gp
import pygraphviz as pgv
import numpy as np
import time
import cPickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import vector_operations
import math, random, operator
''' stuff for saving '''
import os
from PIL import Image

import grower 
import vector_operations
import brain
imp.reload(grower)
imp.reload(vector_operations)
imp.reload(brain)

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

''' create pset '''
pset = brain.big_pset()

''' create fitnessMin and Individual '''
creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

''' toolbox '''
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=5)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def make_phenotype(genome):
    random.seed(30) #make this little section deterministic
    #runner = grower.EvenNutrientsGrower() ###!!!
    runner = grower.Grower.create_fixed_footprint_grower()
    func = toolbox.compile(expr=genome)
    seed = grower.seed_stem(func)
    phenotype = runner.grow_resize_top(seed,t_steps=20)
    random.seed()
    return phenotype

''' fitness evaulator '''
def evalPhenotype(genome, min_health ):
    '''
    Note: must return a tuple value!
    '''
    phenotype = make_phenotype(genome)
    health = phenotype.get_health()
    num_elements = phenotype.number_of_elements()
    if health < min_health:
        # issue with this is it fucks of that stats. Would be better to not-modify score
        # and somehow send signal to not select this. damn
        return 0,-100000 #make sure low health individuals are dominated
    return num_elements, health

''' Saving Shit '''

def _log_fitness(file):
    '''great idea but not reliabling working when load'''
    def decorator(func):
        def wrapper(*args, **kwargs):
            population = func(*args, **kwargs)
            archive = []
            for ind in population:
                x, y = ind.fitness.values
                archive.append( ( float(x), float(y) ) )
            cPickle.dump(archive, file)
            return population
        return wrapper 
    return decorator
# usage: toolbox.decorate("select", log_fitness(open("multi_obj_fit_6.pkl", "wb")))

#MOVED
def log_fitness(big_list):
    def decorator(func):
        def wrapper(*args, **kwargs):
            population = func(*args, **kwargs)
            sub_list = []
            for ind in population:
                x, y = ind.fitness.values
                sub_list.append( ( float(x), float(y) ) )
            big_list.append(sub_list)
            return population
        return wrapper 
    return decorator
# Save an image for each genome in the final population
import mayavi.mlab as mlab

def sort_pop_by_health(pop):
    return sorted(pop, key=lambda x: x.fitness.values[1], reverse=True )

'''  Saving Grid Of Imgs '''

def make_folder(name):
    directory = os.path.join(os.getcwd(), name)
    try:
        os.makedirs(directory)
    except OSError:
        print("folder exists already")
    return directory

def save_images_of_pop(pop,directory):
    '''
    assumes pop is already ordered logically
    and pop has fitness.values
    '''
    for i,genome in enumerate(pop):
        p = make_phenotype(genome)
        p.show_lines()
        n_nodes, health = genome.fitness.values
        info = "{0}. #nodes: {1:.1f}, health: {2:.1f}".format(i, n_nodes, health)
        img_name = str(i).zfill(2)+'_genome.png'
        file_name = os.path.join(directory, img_name)
        p.save_image(info,file_name)

def convert_imgs_to_grid(directory, n_x=8, n_y=10):
    '''
    assumes img size!
    '''
    files = os.listdir(directory)
    im_width = 400
    im_height = 307
    padding = 5
    width = padding + ( im_width + (1 * padding) ) * n_x
    height = padding + ( im_height + (1 * padding) ) * n_y
    new_im = Image.new('RGB', (width, height))
    idx = 0
    for j in xrange(padding, height, im_height + padding):
        for i in xrange(padding, width, im_width + padding):
            file_name = os.path.join(directory, files[idx] )
            im = Image.open( file_name )
            new_im.paste(im, (i,j) )
            idx +=1
    file_name = 'grid_img.png'
    new_im.save(file_name)

def make_grid_img_of_phenotypes(pop):
    directory = make_folder('saved_pop_imgs')
    save_images_of_pop(pop,directory)
    n_img = len(pop)
    def biggest_first_number_factor_pair(val):
        pairs = [(i, val / i) for i in range(1, int(val**0.5)+1) if val % i == 0]
        return pairs[-1]
    n_x, n_y = biggest_first_number_factor_pair(n_img)
    convert_imgs_to_grid(directory, n_x, n_y)

def show_ranked_by_health(rank, pop):
    ranked = sort_pop_by_health(pop)
    g = ranked[rank]
    p = make_phenotype(g)
    p.show()

''' save npz skeleton data '''
def save_skeleton_data(ordered_pop):
    directory = make_folder('saved_skeleton_data')
    for i,genome in enumerate(ordered_pop):
        file_name = os.path.join(directory,"{:02d}_skeleton.npy".format(i))
        p = make_phenotype(genome)
        p.save_line_data(file_name)



#############################################################
## PARAMETERS
N_GEN = 20
print("ngen: {}".format(N_GEN))
N_INDIVID_SELECT = 50 #MU
N_CHILDREN = 100 #LAMBDA
CXPB = 0.6 #crossover .7 originally 
MUTPB = 0.3 #mutation probablity .2 originially
#cloning proablity it 1 - CXPB - MUTPB is 0.1 in this case. 
max_size = 13 #of processor tree
MIN_HEALTH = -50.0


toolbox.register("evaluate", evalPhenotype, min_health=MIN_HEALTH)
toolbox.register("select", tools.selSPEA2) #WORKS right, do not use NSGA2!!
archive = []
toolbox.decorate("select", log_fitness(archive) )
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=2, max_=10)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_size))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_size))

## Genealogy Recording 
history = tools.History()
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate",history.decorator)

def assign_fitness(population):
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

class EvolutionStuff(object):
    ''' organizes stuff from evolution '''
    def __init__(self,final_pop,logbook,hall_of_fame,history,toolbox,pset):
        self.final_pop = final_pop
        self.logbook = logbook
        self.hall_of_fame = hall_of_fame
        self.history = history
        self.toolbox = toolbox
        self.pset = pset

def plot_fitness_over_generations(data):
    v = np.linspace(0, 1, len(data))
    colors = cm.viridis( v )
    fig = plt.figure(figsize=(10,7))
    for i,generation in enumerate(data):
        g = np.array(generation)
        n = g[:,0]
        h = g[:,1]
        plt.scatter(n, h, c=colors[i])
    #plt.scatter(hof[:,0], hof[:,1], s=80, facecolors='none', edgecolors='m')
    #last = np.array(data[-1])
    #plt.scatter(last[:,0], last[:,1], s=80, facecolors='none', edgecolors='m')
    #plt.xlim([-10,100])
    #plt.ylim([-10,200])
    plt.xlabel('number of nodes')
    plt.ylabel('colony health')
    plt.title('nGen: {}'.format(len(data)))
    plt.savefig('fitness_over_generations.pdf')

def main():
    #random.seed(890)

    pop = toolbox.population(n=N_INDIVID_SELECT)
    history.update(pop)
    hof = tools.ParetoFront()

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats_size = tools.Statistics(len)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    pop, log = algorithms.eaMuPlusLambda(pop, 
                                          toolbox, 
                                          N_INDIVID_SELECT, 
                                          N_CHILDREN, 
                                          CXPB, 
                                          MUTPB,
                                          N_GEN, 
                                          stats=stats,
                                          halloffame=hof, 
                                          verbose=True)
    # print log
    
    stuff = EvolutionStuff(pop, log, hof, history, toolbox, pset)
    plot_fitness_over_generations(archive)
    make_grid_img_of_phenotypes(sort_pop_by_health(pop))
    #save npz files
    return stuff,archive

if __name__ == "__main__":
    main()
