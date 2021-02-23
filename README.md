# Test Kit

Exploring how to set up unit tests for Modo Kits

## Setting up a basic Kit

Create an [index.cfg](https://github.com/rondreas/testkit/blob/master/index.cfg) in the kit root, this will tell Modo which paths to include.

In the scripts folder we create a simple *fire-and-forget*

``` python
# python

import lx


def main():
    """ Merge all selected meshes. """
    lx.eval("layer.mergeMeshes true")


if __name__ == '__main__':
    main()
```

This will expose a script in Modo so that when we run `@testkit_merge.py` it will run this script.

In the lxserv we will create a command that Modo will recognize.

``` python
    def basic_Execute(self, msg, flags):
        # We want to use the testkit preset, and revert any potential edits
        lx.eval("preset.fbx testkitFBX")
        lx.eval("preset.fbx.edit revert {}")

        # Get the scene, and all selected meshes
        scene = modo.Scene()
        meshes = scene.selectedByType('mesh')

        scene_dir = os.path.dirname(scene.filename)

        # For each mesh, export them right next to scene.
        for mesh in meshes:
            scene.select(mesh)
            filename = os.path.join(scene_dir, mesh.name + ".fbx")
            lx.command(
                "scene.saveAs",
                filename=filename,
                format="fbx",
                export=True
            )
```

The `basic_Execute` method for commands is main part of what we're doing for now.

This command will depend on a config file defining the preset for our export, to get one just edit the fbx settings in preferences then save the configuration fragment, rename and cleanup the file from any arcane numbers and settings you didn't mean to include. Config can be found [here](https://github.com/rondreas/testkit/blob/98211d790168ca72529064d0e28b44297d8f8c1b/configs/testkit_presets.cfg).

After we've picked a preset we get all selected mesh items. And export each one right next to wherever the current scene (lxo) is saved.

## Adding the first tests

With the basic kit done, we can now move to testing. For this I looked to [Chad Vernons](https://www.chadvernon.com/blog/unit-testing-in-maya/) take on how to set it up to work in Maya.

Being mostly interested now in how to set tests to work with Modos command system, I started with making a simple test for the export. The `startUp` method will run before each test. So here we create the scene, and add primitives to it.

The `tearDown` will attempt to clean up after running our tests so we try keep track of files created so we can remove them, and also we want to close the scene.

``` python
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
```

The test itself will get the path to the scene, so we can remember to remove it during the `tearDown`. Get the expected path for the exported mesh. First check that there is no file, and after the export we will check that we now have one.

``` python
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
```

We will now want to be able to run these tests in Modo, so we create a [script](https://github.com/rondreas/testkit/blob/ccd095cd566833d2d43cde73467a195e86a44724/scripts/testkit_test_runner.py) to do just that.

``` python
    # Get the path to the tests,
    file_svc = lx.service.File()
    kit_root = file_svc.ToLocalAlias('kit_testkit:')
    test_directory = os.path.join(kit_root, 'tests')

    # Add tests to the system path,
    sys.path.insert(0, test_directory)

    # Load the tests as a Test Suite
    suite = unittest.TestLoader().discover(test_directory)

    # And create a Text Test Runner, so the results gets printed
    # to std error, and let's us see the result in the Modo Logs,
    runner = unittest.TextTestRunner()
    runner.failfast = False
    runner.run(suite)
```

This will now allow us to run the tests using `@testkit_test_runner.py` and the result from the tests can be found in the python logs. 

![alt text](https://github.com/rondreas/testkit/blob/master/res/running-first-tests.png?raw=true "Results from running the test")

