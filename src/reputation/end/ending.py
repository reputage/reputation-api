# ================================================== #
#                       ENDING                       #
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

import falcon

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

BASE_PATH = "/reputation"

console = getConsole()

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #

class ReputationResource:
    """
    Reputation resource class.

        Attributes:
        .store - Reference to ioflo data store
    """
    def __init__(self, store=None, **kwa):
        """
        Initialize ReputationResource object.

            Parameters:
            .store - Reference to ioflo data store
        """
        super(**kwa)
        self.store = store

    # ============================================== #

    def on_get(self, req, resp, reputee=None):
        """
        Handles GET requests for a ReputationResource given by query parameter
        with reputee.

            Endpoint:
            /reputation/{{reputee}}

            Headers:
            N/A

            Body:
            N/A

            Parameters:
            req - Falcon request variable
            resp - Falcon response variable
            reputee - Name of reputee
        """
        if reputee is None:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid query is required.')

        result = dbing.getEntry(reputee.lower(), dbn='reputation')
        if result == False:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Reputee could not be found.')
        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(result)

    # ============================================== #

    def on_post(self, req, resp, parameter=None):
        """
        Handles POST requests for a ReputationResource.

            Endpoint:
            /reputation

            Headers:
            N/A

            Body:
            {
              "reputer": "name_of_reputer",
              "reputee": "name_of_reputee",
              "repute":
              {
                "rid" : unique_identifier,
                "feature": "reach or clarity",
                "value": 0 to 10
              }
            }

            Parameters:
            req - Falcon request variable
            resp - Falcon response variable
            parameter - Additional URI variable(s)
        """
        if not parameter is None:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Malformed URI.')
        try:
            rawJson = req.stream.read()
            if not rawJson:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid JSON document is required.')
        except Exception:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid JSON document is required.')

        try:
            jsonObject = json.loads(rawJson)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_422, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

        try:
            reputer = jsonObject['reputer']
            reputee = jsonObject['reputee'].lower()
            rid = str(jsonObject['repute']['rid'])
            feature = jsonObject['repute']['feature']
            value = jsonObject['repute']['value']

            key = reputee + '-' + rid
            ser = json.dumps({"reputer": reputer,
                              "reputee": reputee,
                              "repute": {"rid": rid, "feature": feature, "value": value}})

            try:
                result = dbing.getEntry(reputee.lower(), dbn='preprocessed')

                if result is False:
                    raise falcon.HTTPError(falcon.HTTP_400, 'Entry could not be created.')

                if feature.lower() == "clarity":
                    sum = result['claritySum'] + value
                    length = result['clarityLength'] + 1
                    preprocessed = json.dumps({"claritySum": sum, "clarityLength": length,
                                               "reachSum": result["reachSum"],
                                               "reachLength": result["reachLength"]})
                else:
                    sum = result['reachSum'] + value
                    length = result['reachLength'] + 1
                    preprocessed = json.dumps({"claritySum": result["claritySum"],
                                               "clarityLength": result["clarityLength"],
                                               "reachSum": sum,
                                               "reachLength": length})

                    dbing.putEntry(key, ser)
                    dbing.putEntry(reputee, preprocessed, dbn="preprocessed")
                    dbing.putEntry(reputee, ser, dbn="unprocessed")
                    resp.status = falcon.HTTP_201
                    resp.body = json.dumps({'Message': 'entry successfully created.'})

            except dbing.DatabaseError:
                dbing.putEntry(key, ser)
                dbing.putEntry(reputee, ser, dbn="unprocessed")
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({'Message': 'entry successfully created.'})

        except KeyError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was formatted incorrectly.')

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def loadEnds(app, store):
    """
    Load endpoints for app with store reference. This function
    provides the endpoint resource instances with a reference
    to the data store.

        Parameters:
        app - Falcon application
        store - Ioflo data store
    """
    reputation = ReputationResource()
    app.add_route('{}/'.format(BASE_PATH), reputation)
    app.add_route('{}/{{reputee}}'.format(BASE_PATH), reputation)

# ================================================== #
#                        EOF                         #
# ================================================== #