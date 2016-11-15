import numpy as np


def get_mean_vector(vectors):
    '''
    vectors must be collection of np.array()'s with only one dimension
    all vectors must be same size
    '''
    c = np.column_stack(vectors)
    return np.mean(c,axis=1)    

def get_weighted_average_vectors(vectors,weights_collection):
    n_vec,n_weights = len(vectors),len(weights_collection)
    assert n_vec==n_weights, "number of vectors is {} and should number of weights, {}".format(n_vec,n_weights)
    c = np.column_stack(vectors)
    return np.average(c,axis=1,weights=weights_collection)
