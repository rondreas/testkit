import os

import lx
import lxu
import lxifc

import modo

from testkit_long_running_task import long_running_task


class TestkitExport(lxu.command.BasicCommand):
    """ A very simple exporter. """
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_PreExecute(self, msg):
        # Not keeping it DRY, but we want to simulate us backing files up
        # before we overwrite them in the basic_Execute
        scene = modo.Scene()
        meshes = scene.selectedByType('mesh')
        
        scene_dir = os.path.dirname(scene.filename)

        for mesh in meshes:
            filename = os.path.join(scene_dir, mesh.name + ".fbx")
            if os.path.exists(filename):
                long_running_task(filename)

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

    def cmd_Flags(self):
        """ Seeing we're not making any changes to the scene we should
        be fine using UI instead of Model & Undo

        """
        return lx.symbol.fCMD_UI


lx.bless(TestkitExport, "testkit.export")
