# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
import logging
import importlib
from ..utils.scripts import get_parser

__all__ = ['info']


def main(args=None):
    parser = get_parser(info)
    parser.add_argument('--version', action='store_true',
                        help='Print Gammapy version number')
    parser.add_argument('--tools', action='store_true',
                        help='Print available command line tools')
    parser.add_argument('--dependencies', action='store_true',
                        help='Print available versions of dependencies')
    args = parser.parse_args(args)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    info(**vars(args))


def info(version=False, tools=False, dependencies=False):
    """Print various info on Gammapy to the console.

    TODO: explain.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

    if version:
        _info_version()

    if tools:
        _info_tools()

    if dependencies:
        _info_dependencies()

def _info_version():
    from gammapy import version
    print('\n*** Gammapy version info ***\n')
    print('version: {0}'.format(version.version))
    print('release: {0}'.format(version.release))
    print('githash: {0}'.format(version.githash))
    print('')


def _info_tools():
    # TODO: re-write ... this doesn't work any more
    raise NotImplementedError
    print('\n*** Gammapy tools ***\n')
    # We assume all tools are installed in the same folder as this script
    # and their names start with "gammapy-".
    import os
    from glob import glob
    DIR = os.path.dirname(__file__)
    os.chdir(DIR)
    tools = glob('gammapy-*')
    for tool in tools:
        # Extract first line from docstring as description
        description = 'no description available'
        lines = open(tool).readlines()
        for line in lines:
            if line.startswith('"""'):
                description = line.strip()[3:]
                if description.endswith('"""'):
                    description = description[:-3]
                break
        print('{0:35s} : {1}'.format(tool, description))

    print('')


def _info_dependencies():
    """Print info about Gammapy dependencies."""
    print('\n*** Gammapy dependencies ***\n')
    from gammapy.conftest import PYTEST_HEADER_MODULES

    for label, name in PYTEST_HEADER_MODULES.items():
        try:
            module = importlib.import_module(name)
            version = module.__version__
        except ImportError:
            version = 'not available'

        print('{:>20s} -- {}'.format(label, version))
