
'''
Initialized on 2016/12/16
Josh Lopez-Binder. hi!
based on:
https://github.com/DEAP/deap/blob/a90d3d599aa789a0083f5bc299803ec32d491cbd/examples/gp/symbreg.py
'''

from __future__ import print_function
import sys, imp
import numpy as np
import math, random, operator

import grower 
import brain
import multobj_utils
imp.reload(grower)
imp.reload(brain)
imp.reload(multobj_utils)

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
    #phenotpe = runner.grow(seedm t_steps=20)
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

#############################################################
## PARAMETERS
N_GEN = 1
print("ngen: {}".format(N_GEN))
N_INDIVID_SELECT = 12 #MU
N_CHILDREN = 10 #LAMBDA
CXPB = 0.6 #crossover .7 originally 
MUTPB = 0.3 #mutation probablity .2 originially
#cloning proablity it 1 - CXPB - MUTPB is 0.1 in this case. 
max_size = 13 #of processor tree
MIN_HEALTH = -50.0


toolbox.register("evaluate", evalPhenotype, min_health=MIN_HEALTH)
toolbox.register("select", tools.selSPEA2) #WORKS right, do not use NSGA2!!
archive = []
toolbox.decorate("select", multobj_utils.log_fitness(archive) )
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
    multobj_utils.plot_fitness_over_generations(archive)
    sorted_pop = multobj_utils.sort_pop_by_health(pop)
    multobj_utils.make_grid_img_of_phenotypes(sorted_pop, make_phenotype)
    multobj_utils.save_skeleton_data(sorted_pop, make_phenotype)
    return stuff,archive

if __name__ == "__main__":
    main()
