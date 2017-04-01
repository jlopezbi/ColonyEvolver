import numpy as np
from collections import namedtuple  

def load(file_name='line_data.npy'):
    data = np.load(file_name,encoding='bytes')
    #data is an np array with dimension zero (one element)
    return data[()]

def convert_data(data):
    x = data[b'x']
    y = data[b'y']
    z = data[b'z']
    connections = data[b'connections']
    return x, y, z, connections

def get_full_path(file_name):
    pass

def make_mesh_skeleton(data):
    pass
