import mathutils
from math import radians


def rotate_vec(vector,axis,angle):
    vec = mathutils.Vector(vector)
    vec.rotate(create_rotation_quat(axis,angle))
    return vec

def create_rotation_quat(vector,angle):
    return mathutils.Quaternion(vector,angle)

def make_star_burst(vector,axis,number,angle=360.0):
    '''
    create a polar array of number of vectors, rotated about axis
    '''
    angle_step = radians(angle)/number
    curr_angle = angle_step
    vector = mathutils.Vector(vector)
    vectors = [vector]
    for n in range(number-1):
        v = vector.copy()
        v.rotate(create_rotation_quat(axis,curr_angle))
        curr_angle += angle_step
        vectors.append(v)
    return vectors

def get_ortho(vector):
    '''
    returns a normalized vector, arbitrary rotation, that is 
    orhogonal to the input vector
    '''
    vec = mathutils.Vector(vector)
    ortho_arbitrary = vec.orthogonal()
    ortho_arbitrary.normalize()
    ortho_arbitrary *= vec.length
    return  ortho_arbitrary


