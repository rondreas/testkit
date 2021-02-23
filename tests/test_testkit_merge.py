import os
import tempfile
import unittest

import lx
import modo

class TestkitMergeTest(unittest.TestCase):
    
    def setUp(self):
        # Create a new scene and add some primitives,
        lx.eval("scene.new")
        lx.eval('script.implicit "Unit Cube Item"')
        lx.eval('script.implicit "Unit Sphere Item"')
        lx.eval('script.implicit "Unit Cone Item"')

    def tearDown(self):
        lx.eval("!scene.close")

    def test_merge_all_items(self):
        # Get the scene,
        scene = modo.Scene()

        # Get number of meshes, and assert it's more than one
        number_of_meshes = len(scene.items(itype='mesh'))
        self.assertTrue(number_of_meshes > 1)

        # Select all the meshes,
        scene.select(scene.items(itype="mesh"))

        # Run our merge script
        lx.eval("@testkit_merge.py")

        # And check that the total meshes has dropped to one.
        number_of_meshes = len(scene.items(itype='mesh'))
        self.assertTrue(number_of_meshes == 1)
