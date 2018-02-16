# ================================================== #
#                      HELPING                       #
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
from ..db import dbing

import os
import shutil
import tempfile

try:
    import ujson as json
except ImportError:
    import json

try:
    import msgpack
except ImportError:
    pass

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

console = getConsole()

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def setupTmpBaseDir(baseDirPath=""):
    """
    Setup temporary directory.

        Parameters:
        baseDirPath - Base directory path

        Return:
        Base directory path
    """
    if not baseDirPath:
        baseDirPath = tempfile.mkdtemp(prefix="reputation", suffix="test", dir="/tmp")

    baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
    return baseDirPath

# ================================================== #

def cleanupTmpBaseDir(baseDirPath):
    """
    Remove temporary root of baseDirPath. Ascend tree to
    find temporary root directory.

        Parameters:
        baseDirPath - Base directory path
    """
    if os.path.exists(baseDirPath):
        while baseDirPath.startswith("/tmp/reputation"):
            if baseDirPath.endswith("test"):
                shutil.rmtree(baseDirPath)
                break
            baseDirPath = os.path.dirname(baseDirPath)

# ================================================== #

def cleanupBaseDir(baseDirPath):
    """
    Remove root directory.

        Parameters:
        baseDirPath - Base directory path
    """
    if os.path.exists(baseDirPath):
        shutil.rmtree(baseDirPath)

# ================================================== #

def getAll(reputee, entries=None, reachNum=None, reachDenom=None,
           clarityNum=None, clarityDenom=None):
    """
    Get scores and confidence for reach, clarity, and clout. Creates a
    preprocessed entry if one does not exist.

        Parameters:
        reputee - Name of reputee
        entries - List of reputation entries
        reachNum - Numerator for reach function
        reachDenom - Denominator for reach function
        clarityNum - Numerator for clarity function
        clarityDenom - Denominator for reach function

        Return:
        List of tuples [(clout score, clout confidence),
        (reach score, reach confidence), (clarity score,
        clarity confidence)]
    """
    reachList = []
    clarityList = []

    if not entries is None:
        for entry in entries:
            if entry['reputee'] == reputee:
                if entry['repute']['feature'] == "reach":
                    reachList.append(entry['repute']['value'])
                elif entry['repute']['feature'] == "clarity":
                    clarityList.append(entry['repute']['value'])

        if len(reachList) == 0 and len(clarityList) == 0:
            return False

        try:
            preprocessed = json.dumps({"claritySum": sum(clarityList),
                                       "clarityLength": len(clarityList),
                                       "reachSum": sum(reachList),
                                       "reachLength": len(reachList)})

            dbing.putEntry(reputee, preprocessed, dbn="preprocessed")

        except dbing.DatabaseError:
            pass

        reach = getReach(reachList)
        clarity = getClarity(clarityList)

        if reach is False or clarity is False:
            return False

        clout = getClout(clarity, reach)

    else:
        if (reachNum is None or reachDenom is None or
            clarityNum is None or clarityDenom is None):
            return False
        else:
            reach = getReach(reachNum, reachDenom)
            clarity = getClarity(clarityNum, clarityDenom)

            if reach is False or clarity is False:
                return False

            clout = getClout(clarity, reach)


    return [clout, reach, clarity]

# ================================================== #

def getReach(reachList=None, reachNum=None, reachDenom=None):
    """
    Get scores and confidence for reach.

        Parameters:
        reachList - List of reach values
        reachNum - Numerator for reach function
        reachDenom - Denominator for reach function

        Return:
        Tuple of reach score and reach confidence
    """
    if reachList is None:
        if reachNum is None or reachDenom is None:
            return False

        score = reachNum/reachDenom
        confidence = sFunction(2, 6, reachDenom)

    else:
        if len(reachList) == 0:
            score = 0
        else:
            score = sum(reachList)/len(reachList)
        confidence = sFunction(2, 6, len(reachList))

    return (score, confidence)

# ============================================= #

def getClarity(clarityList=None, clarityNum=None, clarityDenom=None):
    """
    Get scores and confidence for clarity.

        Parameters:
        clarityList - List of clarity values
        clarityNum - Numerator for clarity function
        clarityDenom - Denominator for clarity function

        Return:
        Tuple of clarity score and clarity confidence
    """
    if clarityList is None:
        if clarityNum is None or clarityDenom is None:
            return False

        score = clarityNum/clarityDenom
        confidence = sFunction(4, 8, clarityDenom)

    else:
        if len(clarityList) == 0:
            score = 0
        else:
            score = sum(clarityList) / len(clarityList)
        confidence = sFunction(4, 8, len(clarityList))

    return (score, confidence)

# ============================================= #

def getClout(reach, clarity):
    """
    Get scores and confidence for clout.

        Parameters:
        reach - Reach score
        clarity - Clarity score

        Return:
        Tuple of clout score and clout confidence
    """
    if clarity[1] + reach[1] != 0:
        reachWeight = reach[1]/(clarity[1] + reach[1])
        clarityWeight = clarity[1] / (clarity[1] + reach[1])
    else:
        reachWeight = 0
        clarityWeight = 0

    normalizedWeight = (clarityWeight*clarity[0]) + (reachWeight*reach[0])
    score = normalizedWeight/10
    confidence = min([clarity[1], reach[1]])

    return(score, confidence)

# ============================================= #

def sFunction(a, b, x):
    """
    Sigmoid function for fuzzy set.

        Parameters:
        a - Value of lower bound
        b - Value of upper bound
        x - Value of input variable

        Return:
        Value resulting from S(x)
    """
    if x <= a:
        return 0
    elif a <= x <= ((a+b)/2):
        return 2*((x-a)/(b-a))**2
    elif ((a+b)/2) <= x <= b:
        return 1-2*((x-b)/(b-a))**2
    else:
        return 1

# ================================================== #
#                        EOF                         #
# ================================================== #
