''' module that handles collisions between the growing colony and the nutrients'''
import scipy.spatial as sp
import numpy as np


def collide(tree1,tree2,radius):
    '''
    computes which, if any, members of the colony have been collided
    '''
    neighbor_array = tree1.query_ball_tree(tree2,radius)
    return neighbor_array

def get_points_for_collisions(neighbor_array,tree_other):
    for index_list in neighbor_array:
        if index_list:
            for index in index_list:
                point = tree_other.data[index]


def create_spatial_tree(matrix_collection):
    '''
    creates spatial tree used for efficiently computing collisions
    '''
    spatial_tree = sp.cKDTree(matrix_collection)
    #matrix has shape n data pnts of dimension m
    return spatial_tree

