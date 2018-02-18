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

def test_putGetEntry():
    dbEnv = dbing.setupTestDbEnv()

    ser = "{'reputer': 'Søren', 'reputee': 'Kierkegaard', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f45', " \
          "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key = "søren-dda6555f-21c8-45ff-9633-f9b5cdc59f45"

    dbing.putEntry(key, dat)
    gser = dbing.getEntry(key)
    assert gser == ser

    cleanupTmpBaseDir(dbEnv.path())
    print("test/db/test_dbing: test_putGetEntry() \033[92mPASSED\033[0m")

# ================================================== #

def test_getEntries():
    dbEnv = dbing.setupTestDbEnv()

    ser1 = "{'reputer': 'Søren', 'reputee': 'Kierkegaard', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f45', " \
          "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser1)
    key = "søren-dda6555f-21c8-45ff-9633-f9b5cdc59f45"
    dbing.putEntry(key, dat)

    ser2 = "{'reputer': 'Henrik', 'reputee': 'Ibsen', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f46', " \
           "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser2)
    key = "henrik-dda6555f-21c8-45ff-9633-f9b5cdc59f46"
    dbing.putEntry(key, dat)

    ser3 = "{'reputer': 'Inger', 'reputee': 'Christiansen', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f47', " \
           "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser3)
    key = "inger-dda6555f-21c8-45ff-9633-f9b5cdc59f47"
    dbing.putEntry(key, dat)

    glist = dbing.getEntries()
    assert glist == [ser2, ser3, ser1]

    cleanupTmpBaseDir(dbEnv.path())
    print("test/db/test_dbing: test_getEntries() \033[92mPASSED\033[0m")

# ================================================== #

def test_getEntryKeys():
    dbEnv = dbing.setupTestDbEnv()

    ser = "{'reputer': 'Søren', 'reputee': 'Kierkegaard', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f45', " \
           "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key1 = "søren-dda6555f-21c8-45ff-9633-f9b5cdc59f45"
    dbing.putEntry(key1, dat)

    ser = "{'reputer': 'Henrik', 'reputee': 'Ibsen', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f46', " \
           "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key2 = "henrik-dda6555f-21c8-45ff-9633-f9b5cdc59f46"
    dbing.putEntry(key2, dat)

    ser = "{'reputer': 'Inger', 'reputee': 'Christiansen', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f47', " \
           "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key3 = "inger-dda6555f-21c8-45ff-9633-f9b5cdc59f47"
    dbing.putEntry(key3, dat)

    glist = dbing.getEntryKeys()
    assert [key2, key3, key1]

    cleanupTmpBaseDir(dbEnv.path())
    print("test/db/test_dbing: test_getEntryKeys() \033[92mPASSED\033[0m")

# ================================================== #

def test_deleteEntry():
    dbEnv = dbing.setupTestDbEnv()

    ser = "{'reputer': 'Søren', 'reputee': 'Kierkegaard', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f45', " \
          "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key = "s\u00f8ren-dda6555f-21c8-45ff-9633-f9b5cdc59f45"

    dbing.putEntry(key, dat, dbn="raw")
    gser = dbing.getEntry(key, dbn="raw")
    assert gser == ser

    dbing.deleteEntry(key, dbn="raw")

    with pytest.raises(dbing.DatabaseError):
        dbing.getEntry(key)

    cleanupTmpBaseDir(dbEnv.path())
    print("test/db/test_dbing: test_deleteEntry() \033[92mPASSED\033[0m")

# ================================================== #

def test_deleteEntries():
    dbEnv = dbing.setupTestDbEnv()

    ser = "{'reputer': 'Søren', 'reputee': 'Kierkegaard', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f45', " \
          "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key1 = "s\u00f8ren-dda6555f-21c8-45ff-9633-f9b5cdc59f45"

    dbing.putEntry(key1, dat, dbn="raw")
    gser = dbing.getEntry(key1, dbn="raw")
    assert gser == ser

    ser = "{'reputer': 'Henrik', 'reputee': 'Ibsen', 'repute': {'rid': 'dda6555f-21c8-45ff-9633-f9b5cdc59f46', " \
          "'feature': 'clarity', 'value': 5}})"
    dat = json.dumps(ser)
    key2 = "henrik-dda6555f-21c8-45ff-9633-f9b5cdc59f46"

    dbing.putEntry(key2, dat, dbn="raw")
    gser = dbing.getEntry(key2, dbn="raw")
    assert gser == ser

    dbing.deleteEntries(dbn="raw")

    with pytest.raises(dbing.DatabaseError):
        dbing.getEntry(key1)
        dbing.getEntry(key2)

    cleanupTmpBaseDir(dbEnv.path())
    print("test/db/test_dbing: test_deleteEntries() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #