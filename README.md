SAMI Python SDK demo
================

This is a demo developed to showcase what you can do with the SAMI Python SDK. The demo is developed using some common Python tools such as Django. If you are not familiar with the environment we suggest you first get accustomed to it.

Prerequisites
-------------

 * python 2.7.x: https://www.python.org/download/
 * pip http://pip.readthedocs.org/en/latest/installing.html
 * virtualenvswrapper http://virtualenvwrapper.readthedocs.org/en/latest/install.html
 * Django==1.7
 * argparse==1.2.1
 * httplib2==0.9
 * requests==2.4.3
 * wsgiref==0.1.2

Installation
---------------------

Once you have installed the required libraries add the scripts to your project.

Create a virtualenv with:
	
	$ mkvirtualenv <ENV> 

For example:
	$ mkvirtualenv sami

Switch to your newly created virtualenv:

	$ workon <ENV>

Go to the directory where you copied the scripts
Install with pip the requirements for the demo:

	$ pip install -r requirements.txt

Do a pip freeze to make sure all the packages are correctly installed:

	$ pip freeze

You should get something like this:

	Django==1.7
	argparse==1.2.1
	httplib2==0.9
	requests==2.4.3
	wsgiref==0.1.2

Open `python/settings.py`, check the general settings. At the bottom there are a few parameters that you must configure. If you haven't done so, yet, go to https://devportal.samsungsami.io, authenticate and create an application. Once you have an application in SAMI get the client ID and client secret and store them in `settings.py`.

Now we are ready to start the django. Run the migrate command to start the db:
	$ python manage.py migrate

Then start the server with the command:
	$ python manage.py runserver

Go to your browser and access to http://localhost:8000/

Enjoy!

More about SAMI
---------------

If you are not familiar with SAMI we have extensive documentation at http://developer.samsungsami.io

The full SAMI API specification with examples can be found at http://developer.samsungsami.io/sami/api-spec.html

To create and manage your services and devices on SAMI visit developer portal at http://devportal.samsungsami.io

Licence and Copyright
---------------------

Licensed under the Apache License. See LICENCE.

Copyright (c) 2014 Samsung Electronics Co., Ltd.
