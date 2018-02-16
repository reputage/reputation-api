# ================================================== #
#                     TEST DBING                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: 02/02/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from collections import OrderedDict as ODict
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

def test_setupDbEnv():
    baseDirPath = setupTmpBaseDir()
    assert baseDirPath.startswith("/tmp/reputation")
    assert baseDirPath.endswith("test")
    dbDirPath = os.path.join(baseDirPath, "reputation/db")
    os.makedirs(dbDirPath)
    assert os.path.exists(dbDirPath)

    env = dbing.setupDbEnv(baseDirPath=dbDirPath)
    assert env.path() == dbDirPath

    assert dbing.gDbDirPath == dbDirPath
    assert dbing.gDbEnv is env

    data = ODict()
    dbCore = dbing.gDbEnv.open_db(b'core')

    with dbing.gDbEnv.begin(db=dbCore, write=True) as txn:
        data["name"] = "Søren Kierkegaard"
        data["city"] = "Copenhagen"
        datab = json.dumps(data, indent=2).encode("utf-8")
        txn.put(b'person_0', datab)
        person_0 = txn.get(b'person_0')
        assert person_0 == datab

        data["name"] = "Henrik Ibsen"
        data["city"] = "Skien"
        datab = json.dumps(data, indent=2).encode("utf-8")
        txn.put(b'person_1', datab)
        person_1 = txn.get(b'person_1')
        assert person_1 == datab

        person_0 = txn.get(b'person_0')
        assert person_0 != datab
        data = json.loads(person_0.decode("utf-8"))
        assert data["name"] == "Søren Kierkegaard"
        assert data["city"] == "Copenhagen"

    cleanupTmpBaseDir(dbDirPath)
    assert not os.path.exists(dbDirPath)

    print("test/db/test_dbing: test_setupDbEnv() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #