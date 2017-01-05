'''
Initialized on 2016/12/16
Josh Lopez-Binder. hi.
copied from
https://github.com/DEAP/deap/blob/a90d3d599aa789a0083f5bc299803ec32d491cbd/examples/gp/symbreg.py
'''

import sys, imp
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/')
#TODO: if want other people to use this figure out how to get them this dependency!
import deap.gp as gp
import pygraphviz as pgv
import numpy as np
#import vector_operations
import math, random, operator
import uuid

import plant_grower 
import vector_operations
import brain
imp.reload(plant_grower)
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
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

''' toolbox '''
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

''' fitness evaulator '''
grower = plant_grower.Grower.create_default_grower()
def evalPhenotype(genome,runs):
    '''
    NOte: must return a tuple value!
    '''
    func = toolbox.compile(expr=genome)
    seed = plant_grower.create_seed(func)
    fitness_vals = []
    for run in range(runs):
        # assign a fitness to the individual
        phenotype = grower.grow(seed)
        health = phenotype.get_health()
        size = phenotype.number_of_elements()
        fitness = health+size
        fitness_vals.append(fitness)
    # do some sort of combining of the fitness
    return summarize_values(fitness_vals)

def summarize_values(values):
    return np.average(values),

toolbox.register("evaluate", evalPhenotype, runs=1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    random.seed(318)

    pop = toolbox.population(n=5)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 1, stats=mstats,
                                   halloffame=hof, verbose=True)
    # print log
    return pop, log, hof

if __name__ == "__main__":
    main()
