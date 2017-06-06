''' stuff for saving '''
import os
from PIL import Image

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
