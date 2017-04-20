import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import knapsack

def load_archive(file):
    lists = []
    infile = open(file, 'r')
    while 1:
        try:
            lists.append(pickle.load(infile))
        except (EOFError):
            break
    infile.close()
    return lists

data = load_archive('knapsack_run.pkl')

fig = plt.figure()
f = np.linspace(0,1,len(data))
colors = cm.viridis(f) 
for i,pop in enumerate(data):
    w = []
    v = []
    for ind in pop:
        if ind:
            weight,value = knapsack.evalKnapsack(ind)
            w.append(weight)
            v.append(value)
        plt.scatter(w, v, color=colors[i])

plt.xlabel('weight (trying to minimize)')
plt.ylabel('value, (trying to maximize)')
plt.title('Knapsack problem, multi objective')
plt.show()
