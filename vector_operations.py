import transforms3d
import math
import numpy as np


def rotate_vec(vector,axis,angle_rad):
    quat = create_rotation_quat(axis,angle_rad)
    return transforms3d.quaternions.rotate_vector(vector, quat)

def create_rotation_quat(vector,angle):
    return transforms3d.quaternions.axangle2quat(vector,angle)

def make_star_burst(vector,axis,number,angle=360.0):
    '''
    create a polar array of number of vectors, rotated about axis
    '''
    angle_step = math.radians(angle)/number
    curr_angle = angle_step
    vectors = [vector]
    for n in range(number-1):
        v = np.copy(vector)
        v = rotate_vec(v, axis, curr_angle)
        curr_angle += angle_step
        vectors.append(v)
    return vectors

def get_ortho(vector):
    '''
    returns a vector, same length as input, arbitrary rotation, that is 
    orhogonal to the input vector
    '''
    vector = np.array(vector)
    length = np.linalg.norm(vector)
    ortho_arbitrary = perpendicular_vector(vector)
    ortho_arbitrary = normalize(ortho_arbitrary)
    ortho_arbitrary *= length
    return  ortho_arbitrary

def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector/norm

def perpendicular_vector(v):
    '''
    from: http://codereview.stackexchange.com/questions/43928/algorithm-to-get-an-arbitrary-perpendicular-vector
    '''
    if iszero(v[0]) and iszero(v[1]):
        if iszero(v[2]):
            # v is Vector(0, 0, 0)
            return v
        # v is Vector(0, 0, v.z)
        return np.array([0., 1., 0.])
    return np.array([-v[1], v[0], 0.])

def iszero(number):
    thresh = .001
    if math.fabs(number) <= thresh:
        return True
    else:
        return False

def length(vector):
    return np.linalg.norm(vector)

def get_ortho_np(vector):
    return np.array(get_ortho(vector))


