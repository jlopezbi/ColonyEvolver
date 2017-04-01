import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import mayavi.mlab as mlab

def init_fig():
    fig = mlab.figure()
    return fig

def show_fig():
    mlab.show()

def make_lines(x, y, z, connections):
    '''mayavi setup for drawing many lines.
    x, y, z are numpy arrays of all points
    connections contains lists of indices into the x,y,z arrays
    specifiying lines'''
    points = mlab.points3d(x, y, z,
                          scale_mode='none',
                          scale_factor=0.03)
    points.mlab_source.dataset.lines = connections
    points.mlab_source.reset()
    mlab.pipeline.surface(points,
                          representation='wireframe',
                          line_width = 3)

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
    '''MatplotLib Make axes of 3D plot have equal scale so that spheres appear as spheres,
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



