
'''
Initialized on 2016/12/16
Josh Lopez-Binder. hi.
copied from
https://github.com/DEAP/deap/blob/a90d3d599aa789a0083f5bc299803ec32d491cbd/examples/gp/symbreg.py
'''

from __future__ import print_function
import sys, imp
import deap.gp as gp
import pygraphviz as pgv
import numpy as np
import time
#import vector_operations
import math, random, operator
import uuid

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
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
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
def evalPhenotype(genome,runs):
    '''
    Note: must return a tuple value!
    '''
    target_number_nodes = 13.0
    fitness_vals = []
    #start_time = time.time()
    for run in range(runs):
        phenotype = make_phenotype(genome)
        #health = phenotype.get_health()
        size = phenotype.number_of_elements()
        fitness = math.fabs(target_number_nodes-size)
        fitness_vals.append(fitness)
        #print(".", sep='', end='')
    #end_time = time.time()
    #elapsed = end_time - start_time
    #print("t: "+str(elapsed))
    return summarize_values(fitness_vals)

def summarize_values(values):
    return np.average(values),
#############################################################
## PARAMETERS
POP_SIZE = 40
PHENO_RUNS = 4
N_GEN = 10
max_size = 13 #of processor tree
prob_mate = 0.5
prob_mutate = 0.1

toolbox.register("evaluate", evalPhenotype, runs=PHENO_RUNS)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=7)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_size))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_size))

''' Add Genealogy recorder '''
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
    random.seed()

    pop = toolbox.population(n=POP_SIZE)
    history.update(pop)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, prob_mate, prob_mutate, N_GEN, stats=mstats,
                                   halloffame=hof, verbose=True)
    # print log
    
    stuff = EvolutionStuff(pop, log, hof, history, toolbox, pset)
    return stuff

if __name__ == "__main__":
    main()
