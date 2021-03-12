# python

import os
import sys
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import lx


def main():
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
    with StringIO() as buf:
        runner = unittest.TextTestRunner(stream=buf)
        runner.failfast = False
        runner.run(suite)
        lx.out(buf.getvalue())


if __name__ == '__main__':
    main()
