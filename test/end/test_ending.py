# ================================================== #
#                    TEST ENDING                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: 02/18/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from falcon import testing
from ioflo.base import storing
from pytest import approx

import falcon
import pytest
import reputation.db.dbing as dbing
import reputation.end.ending as ending
import reputation.help.helping as helping
import reputation.prime.priming as priming

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

store = storing.Store(stamp=0.0)

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

@pytest.fixture
def app():
    """
    Create a test WSGI instance
    """
    return testing.TestClient(ending.createApp(store=store))

# ================================================== #

def test_reputationResourceOnGet(app):
    """
    Test GET to reputation endpoint.

        Parameters:
        app - WSGI instance
    """
    priming.setupTest()
    dbing.setupTestDbEnv()

    response = app.simulate_get('/reputation/')
    assert response.content == b'{"title":"Error","description":"A valid query is required."}'
    assert response.status == falcon.HTTP_400

    response = app.simulate_get('/reputation/søren')
    assert response.content == b'{"title":"Error","description":"Reputee could not be found."}'
    assert response.status == falcon.HTTP_400

    ser = json.dumps({"reputee": "søren", "clout": {
                    "score": 5.0},
                    "confidence": 1, "reach": {
                    "score": 5.0,
                    "confidence": 1}, "clarity": {
                    "score": 5.0,
                    "confidence": 1}})
    dbing.putEntry("søren", ser, dbn="reputation")

    response = app.simulate_get('/reputation/søren')
    assert response.content == b'{"reputee":"s\\u00f8ren","clout":{"score":5.0},"confidence":1,"reach":{"score":5.0,' \
                               b'"confidence":1},"clarity":{"score":5.0,"confidence":1}}'
    assert response.status == falcon.HTTP_200

    helping.cleanupTmpBaseDir(dbing.gDbDirPath)

    print("test/end/test_ending: test_reputationResourceOnGet() \033[92mPASSED\033[0m")

# ================================================== #

def test_reputationResourceOnPost(app):
    """
    Test POST to reputation endpoint.

        Parameters:
        app - WSGI instance
    """
    priming.setupTest()
    dbing.setupTestDbEnv()

    response = app.simulate_post('/reputation/søren')
    assert response.content == b'{"title":"Error","description":"Malformed URI."}'
    assert response.status == falcon.HTTP_400

    response = app.simulate_post('/reputation/')
    assert response.content == b'{"title":"Error","description":"A valid JSON document is required."}'
    assert response.status == falcon.HTTP_400

    response = app.simulate_post('/reputation/', body=b'Testing ... 1 ... 2 ... 3')
    assert response.content == b'{"title":"Error","description":"Could not decode the request body. The JSON was malformed or not encoded as UTF-8."}'
    assert response.status == falcon.HTTP_422

    ser = json.dumps({"test":"test"})
    response = app.simulate_post('/reputation/', body=ser)
    assert response.content == b'{"title":"Error","description":"The JSON was formatted incorrectly."}'
    assert response.status == falcon.HTTP_400

    ser = json.dumps({
    "reputer": "Søren",
    "reputee": "Kierkegaard",
    "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f45",
        "feature": "clarity",
        "value": 5
      }
    })
    response = app.simulate_post('/reputation/', body=ser)
    assert response.content == b'{"Message":"entry successfully created."}'
    assert response.status == falcon.HTTP_201

    helping.cleanupTmpBaseDir(dbing.gDbDirPath)

    print("test/end/test_ending: test_reputationResourceOnPost() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #