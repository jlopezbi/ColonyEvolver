
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
#import vector_operations
import math, random, operator

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
    runner = grower.Grower.create_default_grower()
    func = toolbox.compile(expr=genome)
    seed = grower.seed_stem(func)
    return runner.grow(seed,t_steps=20)

''' fitness evaulator '''
def evalPhenotype(genome, runs, max_nodes):
    '''
    Note: must return a tuple value!
    '''
    target_number_nodes = 13.0
    size_scores = []
    health_scores = []
    for run in range(runs):
        phenotype = make_phenotype(genome)
        health = phenotype.get_health()
        num_elements = phenotype.number_of_elements()
        if num_elements > max_nodes:
            return 0, 0 #ensure that bloated phenotypes are avoided; they slow down simulation
        health_scores.append(health)
        size_scores.append(num_elements)
    return summarize_values(size_scores), summarize_values(health_scores)

def summarize_values(values):
    return np.average(values)

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

def log_fitness(big_list):
    def decorator(func):
        def wrapper(*args, **kwargs):
            population = func(*args, **kwargs)
            archive = []
            for ind in population:
                x, y = ind.fitness.values
                archive.append( ( float(x), float(y) ) )
            big_list.append(archive)
            return population
        return wrapper 
    return decorator
# Save an image for each genome in the final population
import mayavi.mlab as mlab

def sort_pop_by_health(pop):
    return sorted(pop, key=lambda x: x.fitness.values[1], reverse=True )

def save_images_of_pop(pop):
    '''
    assumes pop is already ordered logically
    '''
    for i,genome in enumerate(pop):
        p = make_phenotype(genome)
        p.show_lines()
        n_nodes, health = genome.fitness.values
        info = "#nodes: {0:.1f}, health: {1:.1f}".format(n_nodes, health)
        mlab.text(x=0.01, y=0.01, text=info, width=0.9)
        #mlab.title(text='#nodes: {0:.1f}, health:{1:.1f},'.format(n_nodes, health))
        mlab.savefig(str(i).zfill(2)+'_genome.png')
        mlab.close(all=True)
'''
    for i,idx in enumerate(ordered_idx):
        genome = info.final_pop[idx]
        p = ev.make_phenotype(genome)
        p.show_lines()
        mlab.savefig(str(i).zfill(2)+'_genome_'+str(idx)+'.png')
        mlab.close(all=True)
'''

#############################################################
## PARAMETERS
PHENO_RUNS = 7
N_GEN = 20 
N_INDIVID_SELECT = 50 #MU
N_CHILDREN = 100 #LAMBDA
CXPB = 0.7 #crossover 
MUTPB = 0.2 #mutation probablity
max_size = 13 #of processor tree
MAX_NODES = 300 #max size of phenotype in # of nodes

## TEMP PARAMETERS
'''
PHENO_RUNS = 3
N_GEN = 1 
N_INDIVID_SELECT = 50 #MU
N_CHILDREN = 100 #LAMBDA
CXPB = 0.7 #crossover 
MUTPB = 0.2 #mutation probablity
max_size = 13 #of processor tree
MAX_NODES = 300 #max size of phenotype in # of nodes
'''

toolbox.register("evaluate", evalPhenotype, runs=PHENO_RUNS, max_nodes=MAX_NODES)
toolbox.register("select", tools.selNSGA2)
archive = []
toolbox.decorate("select", log_fitness(archive) )
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=7)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_size))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_size))

## Genealogy Recording 
history = tools.History()
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate",history.decorator)

class EvolutionStuff(object):
    ''' organizes stuff from evolution '''
    def __init__(self,final_pop,logbook,hall_of_fame,history,toolbox,pset):
        self.final_pop = final_pop
        self.logbook = logbook
        self.hall_of_fame = hall_of_fame
        self.history = history
        self.toolbox = toolbox
        self.pset = pset

def main():
    random.seed(5)

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
    return stuff,archive

if __name__ == "__main__":
    main()
