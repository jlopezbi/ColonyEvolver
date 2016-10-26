import unittest
import bpy
import sys,os
loc = os.path.dirname(bpy.data.filepath)

loader = unittest.defaultTestLoader
suite = loader.discover(start_dir=loc,pattern='test*.py')
unittest.TextTestRunner(verbosity=2).run(suite)
