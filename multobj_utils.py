''' stuff for saving '''
import os
import shutil
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from PIL import Image

def log_fitness(big_list):
    '''
    to decorate the selection operator in the evolution:
    toolbox.decorate("select", multobj_utils.log_fitness(archive) )
    '''
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

def sort_pop_by_health(pop):
    return sorted(pop, key=lambda x: x.fitness.values[1], reverse=True )

def show_phenotype_ranked_by_health(rank, pop, pheno_maker):
    ranked = sort_pop_by_health(pop)
    g = ranked[rank]
    p = pheno_maker(g)
    p.show()

def make_folder(name):
    '''
    NOTE: will delete existing folder with same directory!
    '''
    directory = os.path.join(os.getcwd(), name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print('owerwrote folder!')
        shutil.rmtree(directory)
        os.makedirs(directory)
    return directory

def save_images_of_pop(pop,directory, pheno_maker):
    '''
    assumes pop is already ordered logically
    and pop has fitness.values
    '''
    for i,genome in enumerate(pop):
        p = pheno_maker(genome)
        p.show_lines()
        n_nodes, health = genome.fitness.values
        info = "{0}. #nodes: {1:.1f}, health: {2:.1f}".format(i, n_nodes, health)
        img_name = str(i).zfill(2)+'_genome.png'
        file_name = os.path.join(directory, img_name)
        p.save_image(info,file_name)

def convert_imgs_to_grid(directory, n_x=8, n_y=10):
    '''
    assumptions: 
        img sizes are same and have size below
        nx and ny multiply to equal num imgs
        directory ONLY contains imgs
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

def make_grid_img_of_phenotypes(pop, pheno_maker):
    directory = make_folder('saved_pop_imgs')
    save_images_of_pop(pop,directory, pheno_maker)
    n_img = len(pop)
    def biggest_first_number_factor_pair(val):
        pairs = [(i, val / i) for i in range(1, int(val**0.5)+1) if val % i == 0]
        return pairs[-1]
    n_x, n_y = biggest_first_number_factor_pair(n_img)
    convert_imgs_to_grid(directory, n_x, n_y)

def save_skeleton_data(ordered_pop, pheno_maker):
    directory = make_folder('saved_skeleton_data')
    for i,genome in enumerate(ordered_pop):
        file_name = os.path.join(directory,"{:02d}_skeleton.npy".format(i))
        p = pheno_maker(genome)
        p.save_line_data(file_name)
