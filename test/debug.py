import mocktest
import pdb
import simpletest
import sys
import tsptest
import unittest


def runUnitTest(testName):
    """ Loads and runs the given test for use
        with python's debugger.

        To use this with the debugger you need to do the following
        in the python interpreter

        >>> execfile('debug.py')
        >>> pdb.run("runUnitTest('mocktest.Test.testClusterConnectivity')")

    """
    sys.argv=['',testName]
    unittest.main()
