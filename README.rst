.. image:: https://github.com/reputage/reputation-api/blob/master/logo/logo.png
   :alt: Reputation API logo
    
|Docs| |Build Status| |codecov.io|

.. |Docs| image:: https://readthedocs.org/projects/reputation-api/badge/?version=latest
   :alt: Reputation Documentation Status on Read The Docs
   
.. |Build Status| image:: https://travis-ci.org/reputage/reputation-api.svg?branch=master
   :alt: Reputation API Status on Travis CI
   
.. |codecov.io| image:: https://codecov.io/gh/reputage/reputation-api/branch/master/graph/badge.svg
   :alt: Reputation API Code Coverage

.. contents::

Overview
========

The reputation API is a simple API implemented in Python 3.6 using the Falcon API framework. It has a POST and a GET endpoint. Data submitted by POST to the API, is stored in a database and processed asynchronously. Processed data can be requested using the GET method. Reputation data for any given reputee includes information on clarity, clout, and reach.

Installation
============

MacOS
-----
Either install Xcode using the app store application or install the Xcode command line tools by using the following terminal command:
:: 
    $ xcode-select --install
Next install Homebrew by using the following terminal command:
::
   $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
Now you can run homebrew using the "brew" command from terminal. Homebrew puts everything in /usr/local so it does not clobber Apple installed libraries and binaries. You may have to to add /usr/local/bin to your bash shell path. You can do this by adding the following to your .bashrc file:

.. code-block:: bash
   
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

You can verify your installation of Homebrew by using the following terminal command:
::
   $ brew doctor
You can upgrade your installation of Homebrew by using the following terminal commands:
::
   $ brew update
   $ brew upgrade
   $ brew doctor
Next, you will need Python 3.6. You can use Homebrew to install this by using the following terminal commands:
::
   $ brew install python3
   $ brew linkapps python3
You can verify your installation of Python 3.6 by using the following terminal command:
::
   $ python3 --version
You can see the path to your Python 3.6 installation by using the following terminal command:
::
   $ which python3
With your download of Python 3.6, there should have been a command-line tool installed on your computer called pip3. To check if pip3 was successfully installed on your machine, open a terminal and run one of the following terminal commands:
::
   $ pip3 -V
   $ pip3 --version
If you recieve the following error message ``bash: pip3: command not found``, you can run the following terminal command to install pip3:
::
   $ sudo easy_install3 pip
With pip3 installed run the following terminal command to update your version of pip3 and install setuptools:
::
   $ pip3 install --upgrade pip setuptools wheel
Next, you will need git. You can use Homebrew to install this by using the following terminal commands:
::
   $ brew install git git-flow git-extras
   $ git config --global credential.helper osxkeychain
   $ brew install git-credential-manager
Next, you will need to download and install the reputation-api source code. You can do this by using the following terminal commands:
::
   $ git clone https://github.com/reputage/reputation-api.git
   $ cd ..
   $ pip3 install -e reputation-api
All of the necessary requirements should have been installed with the last command. If for some reason any of the necessary requirements become uninstalled, you can run the following terminal command from the reputation-api folder to reinstall all of the necessary requirements:
::
   $ pip3 install -r requirements.txt
That completes the MacOS installation process.

Linux (Ubuntu)
-----
Update your distro with the following terminal commands:
::
   $ sudo apt update  
   $ sudo apt upgrade  
   $ sudo apt full-upgrade  
   $ sudo reboot now
Next, you will need Python 3.6. You can install this by using the following terminal commands:
::
   $ wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
   $ tar -zxvf Python-3.6.2.tgz
   $ cd Python-3.6.2
   $ ./configure
   $ make
   $ sudo make install
You can verify your installation of Python 3.6 by using the following terminal command:
::
   $ python3 --version
You can see the path to your Python 3.6 installation by using the following terminal command:
::
   $ which python3
With your download of Python 3.6, there should have been a command-line tool installed on your computer called pip3. To check if pip3 was successfully installed on your machine, open a terminal and run one of the following terminal commands:
::
   $ pip3 -V
   $ pip3 --version
If you recieve the following error message ``bash: pip3: command not found``, you can run the following terminal command to install pip3:
::
   $ sudo easy_install3 pip
With pip3 installed run the following terminal command to update your version of pip3 and install setuptools:
::
   $ pip3 install --upgrade pip setuptools wheel
Next, you will need git. You can install this by using the following terminal commands:
::
   $ sudo apt install git
   $ git config --global credential.helper cache
   $ git config --global credential.https://github.com.username  githubusername
   $ git config --global user.name "githubusername"
   $ git config --global user.email "useremail"
Next, you will need to download and install the reputation-api source code. You can do this by using the following terminal commands:
::
   $ git clone git clone https://github.com/reputage/reputation-api.git
   $ cd ..
   $ sudo -H pip3 install -e reputation-api
All of the necessary requirements should have been installed with the last command. If for some reason any of the necessary requirements become uninstalled, you can run the following terminal command from the reputation-api folder to reinstall all of the necessary requirements:
::
   $ sudo -H pip3 install -r requirements.txt
That completes the Linux (Ubuntu) installation process.

Windows
-------
Coming soon.

Usage
=====

Starting the Service
-------------------
From within the reputation-api folder you can run the API by using the following terminal command:
::
   $ reputationd -v concise -r -p 0.0625 -n reputation -f src/reputation/flo/main.flo -b reputation.core
Alternatively, the API can be run from any location by editing the path specified by the ``-f`` flag. The period at which the API's task scheduler iterates can be edited by changing the value specified by the ``-p`` flag. The console output verbosity can be edited by changing the keyword of the ``-v`` flag.

- The ``-v`` flag controls the verbosity level of the console output. The possible verbosity levels are 'mute', 'terse', 'concise', 'verbose', and 'profuse'.
- The ``-r`` flag runs the scheduler (skedder) in realtime.
- The ``-p`` flag specifies period (time in seconds between iterations of skedder).
- The ``-n`` flag specifies the name of the skedder.
- The ``-f`` flag specifies the path or filename to a flo script.
- The ``-b`` flag specifies the module name to external behavior packages.

POST Requests
-------------
POST requests to the API should hit the endpoint "/reputation" and require a body with a JSON of the following format:

.. code-block:: json

   {
     "reputer": "name_of_reputer",
     "reputee": "name_of_reputee",
     "repute":
     {
       "rid" : "unique_identifier",
       "feature": "reach or clarity",
       "value": 0-10
     }
   }

It is the client's responsibility to ensure that RIDs are unique. It is suggested that RID's be universally unique, but this is not strictly enforced. RID's must, however, be unique per paring of reputer and reputee otherwise they will be discarded. The server will throw an HTTP 400 error if no JSON is sent, an empty JSON is sent, or if a JSON with the wrong formatting is sent. The server will throw a 422 error if the JSON is incorrectly encoded. The server will return a 201 status if the posted data was successfully added to the database or a 200 status if the posted data was already found in the database.

POST requests also require a custom "Signature" header that provides one or more signatures of the request/response body text. The format of the custom Signature header follows the conventions of RFC 7230. The "Signature" header has the following format where tag is replaced with a unique string for each signature value:

::

   Signature: tag = "signature"
      or
   Signature: tag = "signature"; tag = "signature";  ...
  
An example is shown below where one tag is the string signer and the other tag is the string current.

::

   Signature: signer="Y5xTb0_jTzZYrf5SSEK2f3LSLwIwhOX7GEj6YfRWmGViKAesa08UkNWukUkPGuKuu-EAH5U-sdFPPboBAsjRBw=="; current="Xhh6WWGJGgjU5V-e57gj4HcJ87LLOhQr2Sqg5VToTSg-SI1W3A8lgISxOjAI5pa2qnonyz3tpGvC2cmf1VTpBg=="

The tag is the name of a field in the body of the request whose value is a DID from which the public key for the signature can be obtained. If the same tag appears multiple times then only the last occurrence is used. Each signature value is a doubly quoted string ("") that contains the actual signature in Base64 url safe format. By default the signatures are 64 byte EdDSA (Ed25519) signatures that have been encoded into BASE64 url-file safe format. The encoded signatures are 88 characters in length and include two trailing pad characters (==).

An optional tag name is "kind" where the values EdDSA or Ed25519 may be present. The kind tag field value specifies the type of signature. All signatures within the header must be of the same kind. The two tag field values currently supported are did and signer.

GET Requests
------------
GET requests to the API should hit the enpoint "/reputation/{{reputee}}" where {{reputee}} is the name of a reputee. Successful GET requests will return a JSON of the following format:

.. code-block:: json

   {
      "reputee": "name_of_reputee",
      "clout":
      {
        "score": 0-1,
        "confidence": 0-1
      },
      "reach":
      {
        "score": 0-10,
        "confidence": 0-1
      },
      "clarity":
      {
        "score": 0-10,
        "confidence": 0-1
      }
   }
   
The server will throw a 400 error if no reputee query parameter is included in the URL or if the queried reputee cannot be found in the database. A successful GET request will return a 200 status and a JSON.

Testing
=======

The API uses the pytest module for unit testing. Pre-written unit tests are included in the project and can be run by using the following terminal command from the reputation-api folder:
::
   $ pytest
   
Design
======

The API was designed with simplicity, clarity, and performance in mind. It uses ioflo to asynchronously manage a WSGI server and reputation processing. Data at various stages of processing is stored in an LMDB database. API endpoints are set up using the Falcon API framework. The program's command line functionality is implemented using click.

The statistics generated by the server are calculated in the following way:

+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Statistic          | Method                                                                                                            |
+====================+===================================================================================================================+
| Reach Score        |The arithmetic average of all the unique reach POSTs connected with a given reputee.                               |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Reach Confidence   |The result of f(x,a,b) where a = 2, b = 6, and x = the total number of unique reach POSTs connected with a given   |
|                    |reputee.                                                                                                           | 
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Clarity Score      |The arithmetic average of all the unique clarity POSTs connected with a given reputee.                             |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Clarity Confidence |The result of f(x,a,b) where a = 4, b = 8, and x = the total number of unique clarity POSTs connected with a given |
|                    |reputee.                                                                                                           |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Clout Score        |The normalized weighted average of the reach and clarity scores where the weights are the reach and clarity        |
|                    |confidences. A normalized weight is computed by dividing each weight by the sum of the weights. A normalized       |
|                    |weighted average is computed by summing the product of each normalized weight and score then dividing by 10.       |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Clout Confidence   |The minimum of the reach and clarity confidences.                                                                  |
+--------------------+-------------------------------------------------------------------------------------------------------------------+

.. image:: https://camo.githubusercontent.com/cc3abf09a34fe420d5c892cb2337be0abd9453b4/68747470733a2f2f7777772e696a7365722e6f72672f70617065722f412d46555a5a592d42415345442d415050524f4143482d464f522d505249564143592d50524553455256494e472d434c5553544552494e472f496d6167655f3030312e706e67
   :alt: S Function
   
Resources
=========

Below are a list of resources that you may find helpful:

- https://brew.sh
- https://docs.pytest.org
- https://falconframework.org
- https://github.com/ioflo/ioflo_manuals/blob/master/ioflo_FloScriptGuide_v1.6.5.web.pdf
- https://hurl.it
- https://insomnia.rest
- http://ioflo.com
- https://www.python.org
- https://tools.ietf.org/html/rfc7230
