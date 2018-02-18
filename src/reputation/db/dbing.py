# ================================================== #
#                       DBING                        #
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
from ..reputationing import ReputationError

import lmdb
import os

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

MAX_DB_COUNT = 8
DATABASE_DIR_PATH = "/var/reputation/db"
ALT_DATABASE_DIR_PATH = os.path.join('~', '.xaltry/reputation/db')

console = getConsole()
gDbDirPath = None
gDbEnv = None

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #


class DatabaseError(ReputationError):
    """
    Database related errors.

        Example Usage:
        raise DatabaseError("Example error message")
    """

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def setupDbEnv(baseDirPath=None):
    """
    Setup module global variables. If given, use baseDirPath
    parameter, otherwise use DATABASE_DIR_PATH constant.

        Parameters:
        baseDirPath - Base directory path

        Return:
        Module global gDbEnv
    """
    global gDbEnv, gDbDirPath

    if not baseDirPath:
        baseDirPath = DATABASE_DIR_PATH

    baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
    if not os.path.exists(baseDirPath):
        try:
            os.makedirs(baseDirPath)
        except OSError:
            baseDirPath = ALT_DATABASE_DIR_PATH
            baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
            if not os.path.exists(baseDirPath):
                os.makedirs(baseDirPath)
    else:
        if not os.access(baseDirPath, os.R_OK | os.W_OK):
            baseDirPath = ALT_DATABASE_DIR_PATH
            baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
            if not os.path.exists(baseDirPath):
                os.makedirs(baseDirPath)

    gDbDirPath = baseDirPath

    gDbEnv = lmdb.open(gDbDirPath, max_dbs=MAX_DB_COUNT)

    gDbEnv.open_db(b'raw')
    gDbEnv.open_db(b'preprocessed')
    gDbEnv.open_db(b'unprocessed')
    gDbEnv.open_db(b'reputation')

    return gDbEnv

# ================================================== #

def setupTestDbEnv():
    """
    Setup a database environment using a baseDirPath in a
    temporary directory.

        Parameters:
        N/A

        Return:
        Result of setupDbEnv function (module global gDbEnv)
    """
    baseDirPath = setupTmpBaseDir()
    baseDirPath = os.path.join(baseDirPath, "db/reputation")
    os.makedirs(baseDirPath)
    return setupDbEnv(baseDirPath=baseDirPath)

# ================================================== #

def putEntry(key, ser, dbn="raw", env=None):
    """
    Put serialization ser with key key in named sub database
    dbn in lmdb environment env.

        Parameters:
        key - Reputee (or reputee-rid) string associated with
        entry data
        ser - Serialization of repute data
        dbn - Name of LMDB sub database; Default is 'raw'
        env - Main LMDB database environment; Default is None
        (gDbEnv is used if no env is provided)

        Return:
        Boolean
    """
    global gDbEnv

    if env is None:
        env = gDbEnv

    if env is None:
        raise DatabaseError("Database environment is not set up.")

    keyb = key.encode("utf-8")
    serb = ser.encode("utf-8")
    subDb = env.open_db(dbn.encode("utf-8"))
    with env.begin(db=subDb, write=True) as txn:
        result = txn.put(keyb, serb, overwrite=True)

        if not result:
            raise DatabaseError("Entry could not be written to database.")

    return True

# ================================================== #

def getEntry(key, dbn='raw', env=None):
    """
    Get deserialized json data at key key in named sub database dbn
    in lmdb environment env.

        Parameters:
        key - Reputee (or reputee-rid) string associated with
        entry data
        dbn - Name of LMDB sub database; Default is 'raw'
        env - Main LMDB database environment; Default is None
        (gDbEnv is used if no env is provided)

        Return:
        Deserialized json data
    """
    global gDbEnv

    if env is None:
        env = gDbEnv

    if env is None:
        raise DatabaseError("Database environment is not set up.")

    subDb = gDbEnv.open_db(dbn.encode("utf-8"))
    with gDbEnv.begin(db=subDb) as txn:
        serb = txn.get(key.encode("utf-8"))
        if serb is None:
            raise DatabaseError("Resource not found.")

        ser = serb.decode("utf-8")

        try:
            dat = json.loads(ser)
        except ValueError as exception:
            raise DatabaseError("Resource failed desereialization. {}".format(exception))

    return dat

# ================================================== #

def getEntries(dbn='raw', env=None):
    """
    Get list containing deserialized json data of each entry
    in named sub database dbn in lmdb environment env.

        Parameters:
        dbn - Name of LMDB sub database; Default is 'raw'
        env - Main LMDB database environment; Default is None
        (gDbEnv is used if no env is provided)

        Return:
        List of deserialized json data
    """
    global gDbEnv

    if env is None:
        env = gDbEnv

    if env is None:
        raise DatabaseError("Database environment is not set up.")

    entries = []
    subDb = gDbEnv.open_db(dbn.encode("utf-8"), dupsort=True)
    with gDbEnv.begin(db=subDb) as txn:
        with txn.cursor() as cursor:
            if cursor.first():
                while True:
                    value = cursor.value().decode()

                    try:
                        dat = json.loads(value)
                    except ValueError:
                        if cursor.next():
                            continue
                        else:
                            break

                    entries.append(dat)

                    if not cursor.next():
                        break

    return entries

# ================================================== #

def getEntryKeys(dbn='raw', env=None):
    """
    Get list containing key strings of each entry in named sub
    database dbn in lmdb environment env.

        Parameters:
        dbn - Name of LMDB sub database; Default is 'raw'
        env - Main LMDB database environment; Default is None
        (gDbEnv is used if no env is provided)

        Return:
        List of key strings
    """
    global gDbEnv

    if env is None:
        env = gDbEnv

    if env is None:
        raise DatabaseError("Database environment is not set up.")

    entries = []
    subDb = gDbEnv.open_db(dbn.encode("utf-8"), dupsort=True)
    with gDbEnv.begin(db=subDb) as txn:
        with txn.cursor() as cursor:
            if cursor.first():
                while True:
                    value = cursor.key()
                    entries.append(value)

                    if not cursor.next():
                        break

    return entries

# ================================================== #

def deleteEntry(key, dbn='unprocessed', env=None):
    """
    Delete entry at key key in named sub database dbn in lmdb
    environment env.

        Parameters:
        key - Reputee (or reputee-rid) string associated with
        entry data
        dbn - Name of LMDB sub database; Default is 'unprocessed'
        env - Main LMDB database environment; Default is None
        (gDbEnv is used if no env is provided)

        Return:
        Boolean
    """
    global gDbEnv

    if env is None:
        env = gDbEnv

    if env is None:
        raise DatabaseError("Database environment is not set up.")

    subDb = gDbEnv.open_db(dbn.encode("utf-8"), dupsort=True)
    with gDbEnv.begin(db=subDb, write=True) as txn:
        entry = txn.delete(key.encode("utf-8"))
        if entry is None:
            raise DatabaseError("Entry could not be deleted")

    return entry

# ================================================== #

def deleteEntries(dbn='unprocessed', env=None):
    """
    Delete all entries in named sub database dbn in lmdb
    environment env.

        Parameters:
        dbn - Name of LMDB sub database; Default is 'unprocessed'
        env - Main LMDB database environment; Default is None
        (gDbEnv is used if no env is provided)

        Return:
        Boolean
    """
    global gDbEnv

    if env is None:
        env = gDbEnv

    if env is None:
        raise DatabaseError("Database environment is not set up.")

    success = False
    entries = getEntryKeys(dbn=dbn, env=env)

    for entry in entries:
        result = deleteEntry(key=entry.decode("utf-8"), dbn=dbn, env=env)
        if result:
            success = True

    return success

# ================================================== #
#                        EOF                         #
# ================================================== #