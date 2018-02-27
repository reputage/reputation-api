# ================================================== #
#                    TEST HELPING                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: 02/26/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from collections import OrderedDict
from pytest import approx
from reputation.help import helping
from reputation.reputationing import SEPARATOR

import libnacl
import pytest

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def test_parseSignatureHeader():
    """
    Test parsing signature header.
    """
    signature = None
    sigs = helping.parseSignatureHeader(signature)
    assert len(sigs) == 0

    signature = ('did="B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz'
                 'QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg=="')
    sigs = helping.parseSignatureHeader(signature)
    assert sigs['did'] == ("B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz"
                           "QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg==")

    signature = ('did = "B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz'
                 'QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg=="  ;  ')
    sigs = helping.parseSignatureHeader(signature)
    assert sigs['did'] == ("B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz"
                           "QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg==")

    signature = ('did="B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz'
                 'QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg==";'
                 'signer="B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz'
                 'QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg==";'
                 'kind="EdDSA";')
    sigs = helping.parseSignatureHeader(signature)
    assert sigs['did'] == ("B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz"
                           "QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg==")
    assert sigs['did'] == ("B0Qc72RP5IOodsQRQ_s4MKMNe0PIAqwjKsBl4b6lK9co2XPZHLmz"
                           "QFHWzjA2PvxWso09cEkEHIeet5pjFhLUDg==")
    assert sigs['kind'] == "EdDSA"

    print("test/help/test_helping: test_parseSignatureHeader() \033[92mPASSED\033[0m")

# ================================================== #

def test_makeDidSign():
    """
    Testing making DID keys and signature.
    """
    seed = (b'PTi\x15\xd5\xd3`\xf1u\x15}^r\x9bfH\x02l\xc6\x1b\x1d\x1c\x0b9\xd7{\xc0_'
            b'\xf2K\x93`')

    vk, sk = libnacl.crypto_sign_seed_keypair(seed)
    reg = OrderedDict()

    did = helping.makeDid(vk)
    assert did.startswith("did:igo:")
    assert len(did) == 52

    signer = "{}#0".format(did)

    didy, index = signer.rsplit("#", maxsplit=1)
    index = int(index)
    assert index ==  0

    verkey = helping.keyToKey64u(vk)
    kind = "EdDSA"

    reg["did"] = did
    reg["signer"] = signer
    reg["keys"] = [OrderedDict(key=verkey, kind=kind)]

    assert reg["keys"][index]["key"] == verkey
    assert reg == OrderedDict([
        ('did', 'did:igo:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE='),
        ('signer',
            'did:igo:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE=#0'),
        ('keys',
            [
                OrderedDict([
                    ('key', 'Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE='),
                    ('kind', 'EdDSA')
                ])
            ])
    ])

    regser = json.dumps(reg, indent=2)
    assert len(regser) == 244
    assert SEPARATOR not in regser
    assert regser == ('{\n'
                      '  "did":"did:igo:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE=",\n'
                      '  "signer":"did:igo:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE=#0",\n'
                      '  "keys":[\n'
                      '    {\n'
                      '      "key":"Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE=",\n'
                      '      "kind":"EdDSA"\n'
                      '    }\n'
                      '  ]\n'
                      '}')

    regdeser = json.loads(regser)
    assert reg == regdeser
    regserb = regser.encode("utf-8")
    rregser = regserb.decode("utf-8")
    assert rregser == regser

    sig = libnacl.crypto_sign(regserb, sk)[:libnacl.crypto_sign_BYTES]
    assert len(sig) == 64
    signature = helping.keyToKey64u(sig)
    assert len(signature) == 88
    assert signature == ('a5WI7gLrxxaoWlKF62jd_8Pk51Ss7ejcVDSYWVlk7OWF0YcvmJv_Fg7HB39xA4zmHwYyfz9J9dIYYSjp9QBpAg==')

    rsig = helping.key64uToKey(signature)
    assert rsig == sig

    result = helping.verify(sig, regserb, vk)
    assert result

    print("test/help/test_helping: test_makeDidSign() \033[92mPASSED\033[0m")

# ================================================== #

def test_getAll():
    """
    Test getting clarity, reach, and clout.
    """
    entries = []
    result = helping.getAll("Nathan", entries)
    assert result is False

    entries = [{
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
      {
        "rid" : "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
        "feature": "reach",
        "value": 4
      }
    },
    {
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f45",
        "feature": "reach",
        "value": 5
      }
    },
    {
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
        "feature": "reach",
        "value": 6
      }
    },
    {
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
        {
          "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
          "feature": "clarity",
          "value": 7
        }
    },
    {
    "reputer": "Danny",
    "reputee": "Nathan",
    "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f45",
        "feature": "clarity",
        "value": 8
      }
    },
    {
    "reputer": "Danny",
    "reputee": "Nathan",
    "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
        "feature": "clarity",
        "value": 9
      }
    }
    ]

    result = helping.getAll("Nathan", entries)
    assert result[0] == (0.5, 0)
    assert result[1] == (5.0, 0.125)
    assert result[2] == (8.0, 0)

    print("test/help/test_helping: test_getAll() \033[92mPASSED\033[0m")

# ================================================== #

def test_getReach():
    """
    Test getting reach.
    """
    reachList = []
    reach = helping.getReach(reachList)
    assert reach == (0, 0)

    reachList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    reach = helping.getReach(reachList)
    assert reach == (4.5, 1)

    reachList = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    reach = helping.getReach(reachList)
    assert reach == (4.0, 1)

    reachList = [1, 9]
    reach = helping.getReach(reachList)
    assert reach == (5.0, 0)

    reachList = [1, 5, 9]
    reach = helping.getReach(reachList)
    assert reach == (5.0, 0.125)

    reachList = [1, 3, 4, 5, 6, 7, 9]
    reach = helping.getReach(reachList)
    assert reach == (5.0, 1)

    print("test/help/test_helping: test_getReach() \033[92mPASSED\033[0m")

# ================================================== #

def test_getClarity():
    """
    Test getting clarity.
    """
    clarityList = []
    clarity = helping.getClarity(clarityList)
    assert clarity == (0, 0)

    clarityList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    clarity = helping.getClarity(clarityList)
    assert clarity == (4.5, 1)

    clarityList = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    clarity = helping.getClarity(clarityList)
    assert clarity == (4.0, 1)

    clarityList = [1, 9]
    clarity = helping.getClarity(clarityList)
    assert clarity == (5.0, 0)

    clarityList = [1, 5, 9]
    clarity = helping.getClarity(clarityList)
    assert clarity == (5.0, 0)

    clarityList = [1, 3, 4, 5, 6, 7, 9]
    clarity = helping.getClarity(clarityList)
    assert clarity == (5.0, 0.875)

    print("test/help/test_helping: test_getClarity() \033[92mPASSED\033[0m")

# ================================================== #

def test_getClout():
    """
    Test getting clout.
    """
    clout = helping.getClout((0, 0), (0, 0))
    assert clout == (0.0, 0)

    clout = helping.getClout((0, 0), (9, 1))
    assert clout == (0.9, 0)

    clout = helping.getClout((0, 0), (9, 0))
    assert clout == (0.0, 0)

    clout = helping.getClout((1, 0), (1, 1))
    assert clout == (0.1, 0)

    clout = helping.getClout((5, 0.5), (5, 0.5))
    assert clout == (0.5, 0.5)

    clout = helping.getClout((4, 0.875), (5, 0.5))
    assert clout == (0.43636363636363634, 0.5)

    clout = helping.getClout((7, 1), (6, 0.875))
    assert clout == (0.6533333333333333, 0.875)

    print("test/help/test_helping: test_getClout() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #