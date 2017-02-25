import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = [1,2]
y = [1,2]
z = [1,2]
#    1,2,3,4,1,5,1
x = [0,1,1,0,0,0,0]
y = [0,0,1,1,0,0,0]
z = [0,0,0,0,0,1,0]
ax.plot_wireframe(x, y, z )

#ax.plot(x, y, z)
plt.show()
'''

#TODO
# figure out how to clamp range of plot

def init_fig():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    return ax

def show():
    plt.show()

def box_seq(points):
    ''' the hardcoded sequence is set so that
    if one draws a line between conscutive pairs of points, and the points are 0,1,2,3 for the base of a box, and 4,5,6,7 for the top, on draws a wire-frame box'''
    i = [0,1,2,3,0,4,5,1,5,6,2,6,7,3,7,4]
    points = np.array(points)
    seq = points[i]
    seq = np.transpose(seq)
    return seq

def draw_box(points, ax):
    sequence = box_seq(points)
    ax.plot_wireframe(sequence[0], sequence[1], sequence[2])


