# ================================================== #
#                      RESTING                       #
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
from ioflo.aid import odict
from ioflo.aio import WireLog
from ioflo.aio.http import Valet
from ioflo.base import doify
from ..db import dbing
from ..end import ending
from ..prime import priming

import falcon
import os

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

console = getConsole()

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

@doify('ReputationServerOpen', ioinits=odict(valet="",
                                             port=odict(ival=8080),
                                             dbDirPath="",
                                             test="",
                                             preload=""))
def reputationServerOpen(self, buffer=False, **kwa):
    """
    Sets up and opens a rest server.

        Ioinit Attributes:
        valet - Valet instance (wsgi server)
        port - Server port number
        dbDirPath - Directory path for the database
        test - Flag; If True, uses a test configuration if any is
        available
        preload - Flag; If True (and test is True), preloads the
        database for testing

        Parameters:
        buffer - Flag; If True, creates wire log buffer for Valet

        Context:
        enter

        Example Usage:
        do reputation server open at enter
    """
    if buffer:
        wireLog = WireLog(buffify=True, same=True)
        result = wireLog.reopen()
    else:
        wireLog = None

    port = int(self.port.value)
    test = True if self.test.value else False
    preload = True if self.preload.value else False

    if test:
        priming.setupTest()
        if preload:
            dbing.preloadTestDbs()

    else:
        dbDirPath = self.dbDirPath.value if self.dbDirPath.value else None
        dbDirPath = os.path.abspath(os.path.expanduser(dbDirPath)) if dbDirPath else None
        priming.setup(dbDirPath)

        self.dbDirPath.value = dbing.gDbDirPath

        app = falcon.API()
        ending.loadEnds(app, store=self.store)

        self.valet.value = Valet(port=port,
                                 bufsize=131072,
                                 wlog=wireLog,
                                 store=self.store,
                                 app=app,
                                 timeout=0.5)

        result = self.valet.value.servant.reopen()
        if not result:
            console.terse("Error opening server '{0}' at '{1}'\n".format(
                self.valet.name,
                self.valet.value.servant.ha))

            return

        console.concise("Opened server '{0} at '{1}'\n".format(
            self.valet.name,
            self.valet.value.servant.ha))

# ================================================== #


@doify('ReputationServerService', ioinits=odict(valet=""))
def reputationServerService(self, **kwa):
    """
    Service server given by valet.

        Ioinit Attributes:
        valet - Valet instance (wsgi server)

        Parameters:
        N/A

        Context:
        recur

        Example Usage:
        do reputation server service

    """
    if self.valet.value:
        self.valet.value.serviceAll()

# ================================================== #


@doify('ReputationServerClose', ioinits=odict(valet=""))
def reputationServerClose(self, **kwa):
    """
    Closes a valet server.

        Ioinit Attributes:
        valet - Valet instance (wsgi server)

        Parameters:
        N/A

        Context:
        exit

        Example Usgage:
        do reputation server close

    """
    if self.valet.value:
        self.valet.value.servant.closeAll()

        console.concise("Closed server '{0}' at '{1}'\n".format(
            self.valet.name,
            self.valet.value.servant.eha))

# ================================================== #
#                        EOF                         #
# ================================================== #