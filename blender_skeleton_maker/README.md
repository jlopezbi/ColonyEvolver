# Convert a Numpy 3d network to Blender Mesh
This lets you take a numpy representation of a 3d network and turn it intoa blender mesh! 

## Format
The numpy-saved file (.npy) must contain x,y,z point data and c connection data between the points. These are numpy lists, named x, y, z and c. c is a list of lists, each sublist is two indices from the x,y,z data that forms a connection between those points.

## How to use: 
- open a blender file, go to script mode. (or open a text editor window)
- load the make_skeleton.py file
- in the console type
``` from make_skeleton import file_to_skeleton ```
- now in the console type 
``` file_to_skeleton( ```
- drag the .npy file into the console. Close it of with a parenthesis. The path to the file will appear. should looks something like:
``` file_to_skeleton("/Users/josh/Projects/ColonyEvolver_above/ColonyEvolver/line_data.npy") ```
- press enter. A new mesh object will appear called Skeleton!

