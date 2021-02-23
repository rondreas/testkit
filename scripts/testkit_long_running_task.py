import os
import shutil

from time import sleep
from time import time


def long_running_task(filepath):
    """ This will just be a dummy function to simulate a function like speaking
    to a server. It will also perform a behaviour that could be unwanted during
    testing.

    :param filepath: path to the file we want to back up
    :type filepath: str

    """

    sleep(2) # sleep for two seconds.

    # Make a backup copy of the file on the user desktop, as if that wasn't
    # cluttered enough as it is.
    filename = os.path.basename(filepath)
    backup = os.path.join(os.path.expanduser('~'), 'desktop', filename)
    shutil.copyfile(filepath, backup)
