from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
import math
import numpy as np

rmse_accum = Util.ErrorAccumulator()

def gp_add(a, b): return np.add(a,b)
def gp_sub(a, b): return np.subtract(a,b)
def gp_mul(a, b): return np.multiply(a,b)
#def gp_sqrt(a):   return math.sqrt(abs(a))
#def gp_switch(a,b,c): return b if a else c
target_vec = np.array((0.0,0.0,1.0))

n_vec = 10
test_a = [np.random.rand(3) for i in range(n_vec)]
test_b = [np.random.rand(3) for i in range(n_vec)]

def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()
   sum_error = 0
   code_comp = chromosome.getCompiledCode()

   for a in test_a:
       for b in test_b:
         evaluated     = eval(code_comp) #why does this not take inputs?
         #target        = math.sqrt((a*a)+(b*b))
         target        = np.add( np.multiply(a,b), np.subtract(b,a))
         magnitude_diff = np.linalg.norm(np.abs(evaluated-target))
         #rmse_accum   += (target, evaluated)
         sum_error += magnitude_diff
   return sum_error

   #return rmse_accum.getRMSE()

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=3, method="ramped")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a', 'b'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(50)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.25)
   ga.setPopulationSize(800)

   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best

if __name__ == "__main__":
   main_run()
