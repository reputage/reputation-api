# ================================================== #
#                      PRIMING                       #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: 02/15/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from ioflo.aid import getConsole
from ..help.helping import setupTmpBaseDir
from ..db import dbing

import os

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

console = getConsole()

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def setup(dbDirPath=None):
    """
    Setup environments.

        Parameters:
        dbDirPath - Database directory path
    """
    dbEnv = dbing.setupDbEnv(baseDirPath=dbDirPath)

# ================================================== #

def setupTest():
    """
    Setup environments using test values.
    """
    baseDirPath = setupTmpBaseDir()
    dbDirPath = os.path.join(baseDirPath, "reputation/db")
    os.makedirs(dbDirPath)

    setup(dbDirPath=dbDirPath)

# ================================================== #
#                        EOF                         #
# ================================================== #