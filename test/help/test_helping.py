# ================================================== #
#                    TEST HELPING                    #
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
from reputation.help.helping import (getAll, getClarity, getReach, getClout)

import pytest

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def test_getAll():
    """
    Test getting clarity, reach, and clout.
    """
    entries = []
    result = getAll("Nathan", entries)
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

    result = getAll("Nathan", entries)
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
    reach = getReach(reachList)
    assert reach == (0, 0)

    reachList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    reach = getReach(reachList)
    assert reach == (4.5, 1)

    reachList = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    reach = getReach(reachList)
    assert reach == (4.0, 1)

    reachList = [1, 9]
    reach = getReach(reachList)
    assert reach == (5.0, 0)

    reachList = [1, 5, 9]
    reach = getReach(reachList)
    assert reach == (5.0, 0.125)

    reachList = [1, 3, 4, 5, 6, 7, 9]
    reach = getReach(reachList)
    assert reach == (5.0, 1)

    print("test/help/test_helping: test_getReach() \033[92mPASSED\033[0m")

# ================================================== #

def test_getClarity():
    """
    Test getting clarity.
    """
    clarityList = []
    clarity = getClarity(clarityList)
    assert clarity == (0, 0)

    clarityList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    clarity = getClarity(clarityList)
    assert clarity == (4.5, 1)

    clarityList = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    clarity = getClarity(clarityList)
    assert clarity == (4.0, 1)

    clarityList = [1, 9]
    clarity = getClarity(clarityList)
    assert clarity == (5.0, 0)

    clarityList = [1, 5, 9]
    clarity = getClarity(clarityList)
    assert clarity == (5.0, 0)

    clarityList = [1, 3, 4, 5, 6, 7, 9]
    clarity = getClarity(clarityList)
    assert clarity == (5.0, 0.875)

    print("test/help/test_helping: test_getClarity() \033[92mPASSED\033[0m")

# ================================================== #

def test_getClout():
    """
    Test getting clout.
    """
    clout = getClout((0, 0), (0, 0))
    assert clout == (0.0, 0)

    clout = getClout((0, 0), (9, 1))
    assert clout == (0.9, 0)

    clout = getClout((0, 0), (9, 0))
    assert clout == (0.0, 0)

    clout = getClout((1, 0), (1, 1))
    assert clout == (0.1, 0)

    clout = getClout((5, 0.5), (5, 0.5))
    assert clout == (0.5, 0.5)

    clout = getClout((4, 0.875), (5, 0.5))
    assert clout == (0.43636363636363634, 0.5)

    clout = getClout((7, 1), (6, 0.875))
    assert clout == (0.6533333333333333, 0.875)

    print("test/help/test_helping: test_getClout() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #