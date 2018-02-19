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

The reputation API is a simple API implemented in Python 3.6 using the Falcon API framework. It has a POST and a GET endpoint. Data sent in a POST to the API, is stored in the database, and processed asynchronously. Processed data can be requested using the GET method. Processed reputation data for any given reputee includes clarity, clout, and reach scores and confidence.

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
You can run Python 3.6 in the terminal by using the following terminal command:
::
   $ python3
With your download of Python 3.6, there should have been a command-line tool installed on your computer called pip3. To check if pip3 was successfully installed on your machine, open a terminal and run one of the following terminal commands:
::
   $ pip3 -V
   $ pip3 --version
If you recieve the following error message: 
::
   bash: pip3: command not found
You can run the following terminal command to install pip3:
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
   $ git clone git clone https://github.com/reputage/reputation-api.git
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
If you recieve the following error message: 
::
   bash: pip3: command not found
You can run the following terminal command to install pip3:
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
Alternatively, the API can be run from any location by editing the path specified by the ``-f`` flag. The period at which the API's task scheduler iterates can be edited by changing the value specified by the ``-p``. The console output verbosity can be edited by changing the keyword of the ``-v`` flag.

- The ``-v`` flag controls the verbosity level of the console output. The possible verbosity levels are 'mute', 'terse', 'concise', 'verbose', and 'profuse'.
- The ``-r`` flag runs the scheduler (skedder) in realtime.
- The ``-p`` flag specifies period (time in seconds between iterations of skedder).
- The ``-n`` flag specifies the name of the skedder.
- The ``-f`` flag specifies the path or filename to a flo script.
- The ``-b`` flag specifies the module name to external behavior packages.

POST Requests
-------------
POST requests to the API should hit the endpoint "/reputation", and require a body comprised of a JSON with the following format:
.. code-block:: json

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
