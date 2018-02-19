.. image:: https://github.com/reputage/reputation-api/blob/master/logo/logo.png
   :alt: Reputation API logo
    
|Docs| |Build Status| |codecov.io|

.. |Docs| image:: https://readthedocs.org/projects/reputation-api/badge/?version=latest
   :alt: Reputation Documentation Status on Read The Docs
   
.. |Build Status| image:: https://travis-ci.org/reputage/reputation-api.svg?branch=master
   :alt: Reputation API Status on Travis CI
   
.. |codecov.io| image:: https://codecov.io/gh/reputage/reputation-api/branch/master/graph/badge.svg
   :alt: Reputation API Code Coverage

Overview
========

The reputation API is a simple API implemented in Python 3.6 using the Falcon API framework. It has a POST and a GET endpoint. Data sent in a POST to the API, is stored in the database, and processed asynchronously. Processed data can be requested using the GET method. Processed reputation data for any given reputee includes clarity, clout, and reach scores and confidence.

Installation
============

MacOS
-----
Either install Xcode using the app store application or install only the Xcode command line tools with the following terminal command:
:: 
    $ xcode-select --install
Next install Homebrew with the following terminal command:
::
   $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
Now you can run homebrew using the "brew" command from terminal. Homebrew puts everything in /usr/local so it does not clobber Apple installed libraries and binaries. You may have to to add /usr/local/bin to your bash shell path. You can do this by adding the following to your .bashrc file:

.. highlight:: bash
   #Add paths for non-interactive non-login shells such as ssh remote command
   
   # /usr/local/sbin prepend
   echo $PATH | grep -q -s "/usr/local/sbin"
   if [ $? -eq 1 ] ; then
      PATH=/usr/local/sbin:${PATH}
      export PATH
   fi
   
   # /usr/local/bin prepend
   echo $PATH | grep -q -s "/usr/local/bin"
   if [ $? -eq 1 ] ; then
      PATH=/usr/local/bin:${PATH}
      export PATH
   fi
   
   echo $MANPATH | grep -q -s "/usr/local/share/man"
   if [ $? -eq 1 ] ; then
      MANPATH=/usr/local/share/man:${MANPATH}
      export MANPATH
   fi
   
   # If not running interactively, don't do anymore just return so sftp works:
   [ -z "$PS1" ] && return

