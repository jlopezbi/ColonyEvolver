import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import mayavi.mlab as mlab
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
    pass

def show_fig(ax):
    mlab.show()

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

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

