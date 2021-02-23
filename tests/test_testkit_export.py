import os
import tempfile
import unittest

import lx

class TestkitExportTest(unittest.TestCase):

    # Keep track of files and scenes we've created,
    files = list()
    
    def setUp(self):
        """ This will be executed before any of the test methods we
        create. 

        """

        # Create a scene and rember it's index
        lx.eval("scene.new")

        # In this scene, create three primitives,
        lx.eval('script.implicit "Unit Cube Item"')
        lx.eval('script.implicit "Unit Sphere Item"')
        lx.eval('script.implicit "Unit Cone Item"')

        # Save the scene to a temporary directory
        directory = tempfile.mkdtemp()
        filepath = os.path.join(directory, 'test_scene.lxo')
        lx.eval("scene.saveAs {%s}" % (filepath))

        self.files.append(filepath)

        # We could also create and set a default scene through 
        # `application.defaultScene`
        # Or load a scene that we want our tests to run in.

    def tearDown(self):
        """ And this will be executed after the test finishes. """

        # Delete the files we've created.
        for f in self.files:
            if os.path.exists(f):
                os.remove(f)

        # Forget previous list, and be ready to remember files from next test
        self.files = list()

        # Close the current scene, no questions asked.
        lx.eval("!scene.close")

    def test_export_single_item(self):
        # Get the filepath for the current scene,
        scene_path = lx.eval('query sceneservice scene.file ? current')
        scene_dir = os.path.dirname(scene_path)
        fbx = os.path.join(scene_dir, "Sphere.fbx")

        self.files.append(fbx)

        # We haven't exported any, but let's make sure
        self.assertFalse(os.path.exists(fbx))

        # Select the Sphere and export it,
        lx.eval("select.subItem Sphere set mesh;")
        lx.eval("testkit.export")

        # Now that we've exported our Sphere, let's check that we have an
        # fbx next to the lxo.
        self.assertTrue(os.path.exists(fbx))

    def test_export_with_backup(self):
        scene_path = lx.eval('query sceneservice scene.file ? current')
        scene_dir = os.path.dirname(scene_path)
        fbx = os.path.join(scene_dir, "Cone.fbx")

        self.files.append(fbx)

        self.assertFalse(os.path.exists(fbx))

        # Select the Cone and export it,
        lx.eval("select.subItem Cone set mesh;")
        lx.eval("testkit.export")

        # Check that we indeed did export a Cone.fbx
        self.assertTrue(os.path.exists(fbx))

        # Oh shoot, we forgot the unit cone is not planted to the floor,
        # let's fix that and export again. If we wanted it as before we
        # can always find the backup on desktop where it belongs.
        lx.eval("transform.channel pos.Y 0.75")
        lx.eval("testkit.export")

        # Assert we still have an exported Cone.fbx
        self.assertTrue(os.path.exists(fbx))
