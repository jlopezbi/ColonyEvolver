import unittest
#import bpy
#import sys,os
#loc = os.path.dirname(bpy.data.filepath)
loc = '.'   


if __name__=="__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=loc,pattern='test*.py',top_level_dir=loc)
    unittest.TextTestRunner(verbosity=2).run(suite)
