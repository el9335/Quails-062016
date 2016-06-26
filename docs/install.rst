.. _install: 

============
Installation
============

This page will guide you through installing Quails and its dependencies on a unix-based operating system.  Quails currently only supports python 2.7.6.  The next iteration will automatically install all dependencies.

These instructions have been used to install Quails on a fresh Ubuntu Server 14.04.2 LTS.  If you run into any errors during the process, please send me an email at ``leblanc at drexel dot edu``.

View the git project at
::

	https://github.com/el9335/QUAILS_1.0

Download the project from your terminal using
::

	git clone https://github.com/el9335/QUAILS_1.0

See step 9 below for command to install git if necessary.

Steps to install dependencies
=============================
Perform these operations in the QUAILS_1.0 directory after cloning the repository.

One of the dependencies requires Java, so if it is not already installed on your machine, install using the following:
::

	sudo apt-get install default-jre-<your_version> 

1.  Install pip
::

	sudo apt-get install python-pip

2.  Install python-dev
::

	sudo apt-get install python-dev

3.  Install Python's ConfigParser
::

	sudo pip install configparser

4.  Install the Python Requests library
::
	
	sudo pip install requests

5.  Install the Flask RESTful server library
::
	
	sudo pip install flask

6.  Install Natural Language ToolKit
::
	
	sudo pip install nltk

7.  From the command line open a Python interpreter instance and enter the following lines:
::

	import nltk
	nltk.download('all')

Something in the nltk download script causes it to fail, so if/when it happens, just exit the interpreter.  The next version will include a workaround to shield the user from this issue.

8.  Install pexpect, unidecod, and jsonrpclib, all required to run the Stanford Core libraries.
::
	
	sudo pip install pexpect unidecode jsonrpclib

9.  Install git (if not already installed)
::

	sudo apt-get install git

10. Install the corenlp-python library
::

	git clone https://bitbucket.org/torotoki/corenlp-python.git
	cd corenlp-python.git
	sudo python setup.py install

11. Install the Stanford Core NLP Jars in the top level project directory(``sudo apt-get install wget`` if not already installed)
::
	cd ..
	wget http://nlp.stanford.edu/software/stanford-core-nlp-full-2014-08-27.zip
	unzip stanford-corenlp-full-2014-08-27.zip

You may need to install unzip depending on the machine you are installing on.  
::

	sudo apt-get install unzip

12. Install numpy, scipy, and sklearn
::

	sudo apt-get install python-numpy python-scipy
	sudo pip install scikit-learn

13. Install whoosh text indexer for Python
::
	
	sudo pip install whoosh

14. Start the server
:: 
	python serv.py

15. Refer to the Asking a Question section of this documentation to continue working with quails.
