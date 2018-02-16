# ================================================== #
#                    TEST PRIMING                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from pytest import approx
from reputation.db import dbing
from reputation.help.helping import setupTmpBaseDir, cleanupTmpBaseDir
from reputation.prime import priming

import os
import pytest

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def test_setupPrime():
    baseDirPath = setupTmpBaseDir()
    assert baseDirPath.startswith("/tmp/reputation")
    assert baseDirPath.endswith("test")

    dbDirPath = os.path.join(baseDirPath, "reputation/db")
    os.makedirs(dbDirPath)
    assert os.path.exists(dbDirPath)

    priming.setup(dbDirPath=dbDirPath)
    assert dbing.gDbDirPath == dbDirPath

    cleanupTmpBaseDir(baseDirPath)
    assert not os.path.exists(baseDirPath)

    print("test/prime/test_priming: test_setupPrime() \033[92mPASSED\033[0m")

# ================================================== #

def test_setupTestPrime():
    priming.setupTest()
    assert os.path.exists(dbing.gDbDirPath)

    cleanupTmpBaseDir(dbing.gDbDirPath)
    assert not os.path.exists(dbing.gDbDirPath)

    print("test/prime/test_priming: test_setupTestPrime() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #