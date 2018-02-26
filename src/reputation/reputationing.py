# ================================================== #
#                   REPUTATIONING                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

DID_LENGTH = 52
SEPARATOR = "\r\n\r\n"
SEPARATOR_BYTES = SEPARATOR.encode("utf-8")

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #

class ReputationError(Exception):
    """
    Base class for reputation exception
    """
# ================================================== #

class ValidationError(ReputationError):
    """
    Class for validation related errors
    """

# ================================================== #
#                        EOF                         #
# ================================================== #
