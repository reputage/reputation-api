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

from collections import OrderedDict
from ioflo.aid import getConsole
from .. import reputationing
from ..db import dbing

import base64
import libnacl
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

def parseSignatureHeader(signature):
    """
    Parses header of http calls. Signature header has format:
    Signature: headervalue
    Headervalue: tag = "signature"
    or
    tag = "signature"; tag = "signature"  ...
    where tag is the name of a field in the body of the request the value
    of which is a DID where the public key for the signature can be obtained.
    If the same tag appears multiple times, only the last occurrence is returned.
    Each signature value is a doubly quoted string that contains the actual signature
    in Base64 url safe format. By default the signatures are EdDSA (Ed25519)
    which are 88 characters long (with two trailing pad bytes) that represent
    64 byte EdDSA signatures. An option tag name = "kind" with values "EdDSA"
    "Ed25519" may be present that specifies the type of signature. All signatures
    within the header must be of the same kind. The two tag fields currently
    supported are "did" and "signer".

        Parameters:
        signature - Signature to be parsed

        Return:
        ODict of fields and values parsed from signature which is the
        value portion of a Signature header
    """
    sigs = OrderedDict()
    if signature:
        clauses = signature.split(";")
        for clause in clauses:
            clause = clause.strip()
            if not clause:
                continue
            try:
                tag, value = clause.split("=", maxsplit=1)
            except ValueError:
                continue
            tag = tag.strip()
            if not tag:
                continue
            value = value.strip()
            if not value.startswith('"') or not value.endswith('"') or len(value) < 3:
                continue
            value = value[1:-1]
            value = value.strip()
            sigs[tag] = value

    return sigs

# ================================================== #

def keyToKey64u(key):
    """
    Convert key to unicode base64 url-file safe version.

        Parameters:
        key - Key to be encoded

        Return:
        Encoded bytes key
    """
    return base64.urlsafe_b64encode(key).decode("utf-8")

# ================================================== #

def key64uToKey(key64u):
    """
    Convert unicode base64 url-file safe key64u to bytes key

        Parameters:
        key64u - Unicode base64 encoded key

        Return:
        Decoded bytes key
    """
    return base64.urlsafe_b64decode(key64u.encode("utf-8"))

# ================================================== #

def makeDid(vk, method="igo"):
    """
    Create and return Xaltry DID from bytes vk.

        Parameters:
        vk - 32 byte verifier key from EdDSA (Ed25519) key pair

        Return:
        DID string
    """
    vk64u = keyToKey64u(vk)
    did = "did:{}:{}".format(method, vk64u)
    return did

# ================================================== #

def makeTestDid():
    """
    Create and return test DID from bytes vk.

        Return:
        Tuple (DID string, secret key)
    """
    seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)
    publicKey, secretKey = libnacl.crypto_sign_seed_keypair(seed)

    return (makeDid(publicKey), secretKey)

# ================================================== #

def signResource(resource, sk):
    """
    Cryptographically signs a resource.

        Parameters:
        resource - Resource to be signed
        sk - signing secret key

        Return:
        Encoded bytes key
    """
    sig = libnacl.crypto_sign(resource, sk)
    sig = sig[:libnacl.crypto_sign_BYTES]

    return keyToKey64u(sig)

# ================================================== #

def verify(sig, msg, vk):
    """
    Checks if signature sig of message msg is verifiable with
    verification key vk.

        Parameters:
        sig - Signature byte string
        msg - Message byte string
        vk - Verification key byte string

        Return:
        Boolean
    """
    try:
        result = libnacl.crypto_sign_open(sig + msg.decode('utf-8').encode(), vk)
    except Exception as exception:
        return False
    return (True if result else False)

# ================================================== #


def verify64u(signature, message, verkey):
    """
    Checks if signature is valid for message with respect to verification
    key verkey.

        Parameters:
        signature - Unicode base64 url-file encoded signature
        message - Unicode base64 url-file encoded message
        verkey - Unicode base64 url-file encoded verification key

        Return:
        Boolean
    """
    sig = key64uToKey(signature)
    vk = key64uToKey(verkey)
    return (verify(sig, message, vk))

# ================================================== #

def extractDatSignerParts(dat, method="igo"):
    """
    Parses DID index keystr from signer field value of dat.
    Raises ValueError if parsing fails.

        Parameters:
        dat - Data to be parsed
        method - Method string used to generate DID's in the resource

        Return:
        Tuple (did, index, keystr)
    """
    try:
        did, index = dat["signer"].rsplit("#", maxsplit=1)
        index = int(index)
    except (KeyError, ValueError):
        raise ValueError("Missing signer field or invalid indexed signer value")

    try:
        pre, meth, keystr = did.split(":")
    except ValueError:
        raise ValueError("Malformed DID value")

    if pre != "did" or meth != method:
        raise ValueError("Invalid DID value")

    return (did, index, keystr)

# ================================================== #

def extractDidSignerParts(signer, method="igo"):
    """
    Parses DID index keystr from signer key indexed at DID.
    Raises ValueError if parsing fails.

        Parameters:
        signer - Signer key
        method - Method string used to generate DID's in the resource

        Return:
        Tuple (did, index, keystr)
    """
    try:
        did, index = signer.rsplit("#", maxsplit=1)
        index = int(index)
    except ValueError:
        raise ValueError("Invalid indexed signer value")

    try:
        pre, meth, keystr = did.split(":")
    except ValueError:
        raise ValueError("Malformed DID value")

    if pre != "did" or meth != method:
        raise ValueError("Invalid DID value")

    return (did, index, keystr)

# ================================================== #

def extractDidParts(did, method="igo"):
    """
    Parses keystr from DID. Raises ValueError if parsing fails.

        Parameters:
        did - DID string
        method - Method string used to generate DID's in the resource

        Return:
        Parsed key string
    """
    try:
        pre, meth, keystr = did.split(":")
    except ValueError:
        raise ValueError("Malformed DID value")

    if pre != "did" or meth != method:
        raise ValueError("Invalid DID value")

    return keystr

# ================================================== #

def validateSignedResource(signature, resource, verkey, method="igo"):
    """
    Validates signature for a given resource.

        Parameters:
        signature - Base64 url-file safe unicode string signature generated
        by signing bytes version of resource with private signing key associated with
        public verification key referenced by key indexed signer field in resource
        resource - JSON encoded unicode string of resource record
        verkey - Base64 url-file safe unicode string public verification key referenced
        by signer field in resource. This is looked up in database from signer's
        agent data resource
        method - Method string used to generate DID's in the resource

        Return:
        Dictionary of deserialized resource (if signature verifies for resource given
        verification key verkey in base64 url safe unicode format) or None
    """

    try:
        try:
            rsrc = json.loads(resource)
        except ValueError:
            raise reputationing.ValidationError("Invalid JSON")

        if not rsrc:
            raise reputationing.ValidationError("Empty body")

        if not isinstance(rsrc, dict):
            raise reputationing.ValidationError("JSON not dict")

        if "reputee" not in rsrc:
            raise reputationing.ValidationError("Missing did field")

        ddid = rsrc["reputee"]

        try:
            pre, meth, keystr = ddid.split(":")
        except ValueError:
            raise reputationing.ValidationError("Invalid format did field")

        if pre != "did" or meth != method:
            raise reputationing.ValidationError("Invalid format did field")

        if len(verkey) != 44:
            raise reputationing.ValidationError("Verkey invalid")

        if not verify64u(signature, resource, verkey):
            raise reputationing.ValidationError("Unverifiable signature")

    except reputationing.ValidationError:
        raise

    except Exception:
        raise reputationing.ValidationError("Unexpected error")

    return rsrc

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
