import bpy
import mathutils
import numpy as np
import math


def create_metaball_obj(resolution=.05,obj_name=None,metaball_name=None):
    #appears that 'metaball' name is reserved
    if obj_name == None: obj_name = "MyMetaballObject"
    if metaball_name==None: metaball_name = "MyMetaball"
    mball = bpy.data.metaballs.new(metaball_name)
    mball.resolution = resolution
    obj = bpy.data.objects.new(obj_name,mball)
    bpy.context.scene.objects.link(obj)
    return obj,mball


def add_metaball_rod(mball,radius,start,end):
    ele = mball.elements.new()
    ele.type = 'CAPSULE'
    ele.co = get_average_vector((start,end)) #centered
    ele.rotation = get_quaternion(start,end)
    ele.size_x = distance(start,end)/2.0 #size is from center to end of rod
    ele.use_negative = False
    ele.radius = radius
    return ele

def get_quaternion(start,end):
    #vec = end-start
    vec = mathutils.Vector(end-start)
    quat = vec.to_track_quat('X','Z')
    quat.normalize()
    return quat

def distance(start,end):
    return np.linalg.norm(end-start)

def get_average_vector(vectors):
    '''
    vectors must be tuple of np.array()'s with only one dimension
    all vectors must be same size
    '''
    c = np.column_stack(vectors)
    return np.mean(c,axis=1)


         



    
