# Convert .NPY 3d network to Mesh Skeleton
This lets you take a .npy file that contains x,y,z point data and c connection data between the points. c is a list of lists, each sublist is two indices from the x,y,z data that forms and edge or a connection between those points.

## How to use: 
- open a blender file, go to script mode. (or open a text editor window)
- load the make_skeleton.py file
- in the console type
``` from make_skeleton import file_to_skeleton ```
- now in the console type 
``` file_to_skeleton( ```
- drag the .npy file into the console. The path to the file will appear. should looks something like:
``` file_to_skeleton("/Users/josh/Projects/ColonyEvolver_above/ColonyEvolver/line_data.npy") ```
- press enter. A new mesh object will appear called Skeleton.

