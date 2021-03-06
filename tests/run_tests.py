# -*- coding: utf-8 -*-

##########################################################################
# Copyright (c) 2017-2018 Bertrand Néron. All rights reserved.                #
# Use of this source code is governed by a BSD-style license that can be #
# found in the LICENSE file.                                             #
##########################################################################


import unittest
import sys
import os



def discover(test_files=None, test_root_path=None):
    if not test_root_path:
        test_root_path = os.path.dirname(__file__)

    if not test_files:
        suite = unittest.TestLoader().discover(test_root_path, pattern="test_*.py")

    else:
        test_files = [os.path.abspath(f) for f in test_files]
        test_files = [t for t in test_files if test_root_path in t]
        suite = unittest.TestSuite()
        for test_file in test_files:
            if os.path.exists(test_file):
                if os.path.isfile(test_file):
                    fpath, fname = os.path.split(test_file)
                    suite.addTests(unittest.TestLoader().discover(fpath, pattern=fname))
                elif os.path.isdir(test_file):
                    suite.addTests(unittest.TestLoader().discover(test_file))
            else:
                sys.stderr.write("{0} : no such file or directory\n".format(test_file))

    return suite



def run_tests(test_files, verbosity=0):
    """
    Execute Unit Tests

    :param test_files: the file names of tests to run.
    of it is empty, discover recursively tests from 'tests/unit' directory.
    a test is python module with the test_*.py pattern
    :type test_files: list of string
    :param verbosity: the verbosity of the output
    :type verbosity: positive int
    :return: True if the test passed successfully, False otherwise.
    :rtype: bool
    """
    test_root_path = os.path.abspath(os.path.dirname(__file__))
    suite = discover(test_files, test_root_path)
    test_runner = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return test_runner


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("tests",
                        nargs='*',
                        default=False,
                        help="name of test to execute")

    parser.add_argument("-v", "--verbose",
                        dest="verbosity",
                        action="count",
                        help="set the verbosity level of output",
                        default=0
                        )

    args = parser.parse_args(args)

    result_all_tests = []

    EMG_HOME = os.path.abspath(os.path.join(__file__, '..', '..'))

    print("\n", "#" * 70, sep='')
    print("Test Runner: Unit tests")
    print("#" * 70)

    old_path = sys.path

    if EMG_HOME not in sys.path:
        # need to add
        sys.path.insert(0, EMG_HOME)
    test_runner = run_tests(args.tests, verbosity=args.verbosity)
    unit_results = test_runner.wasSuccessful()
    sys.path = old_path
    return unit_results



if __name__ == '__main__':

    unit_results = main(sys.argv[1:])
    if unit_results:
        sys.exit(0)
    else:
        sys.exit(1)