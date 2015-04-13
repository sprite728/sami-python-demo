SAMI Python SDK demo
================

This is a demo developed to showcase what you can do with the SAMI Python SDK. The demo is developed using some common Python tools such as Django. If you are not familiar with the environment we suggest you first get accustomed to it.

Prerequisites
-------------

 1 python 2.7.x: https://www.python.org/download/
 2 pip http://pip.readthedocs.org/en/latest/installing.html
 3 virtualenvswrapper http://virtualenvwrapper.readthedocs.org/en/latest/install.html
 4 Django==1.7
 5 argparse==1.2.1
 6 httplib2==0.9
 7 requests==2.4.3
 8 wsgiref==0.1.2
 9 SAMI Python SDK https://github.com/samsungsamiio/sami-python

Installation
---------------------

Install the first three required libraries, and then install the rest of them as follows:

 * Create a virtualenv with:
	
~~~
	$ mkvirtualenv <ENV> 
~~~

  For example: $ mkvirtualenv sami

 * Switch to your newly created virtualenv:

~~~
	$ workon <ENV>
~~~

 * Go to the root directory of the demo app.
 * Install with pip the requirements for the demo:

~~~
	$ pip install -r requirements.txt
~~~

 * Do a pip freeze to make sure all the packages are correctly installed:

~~~
	$ pip freeze
~~~

   You should get something like this:

~~~
	Django==1.7
	argparse==1.2.1
	httplib2==0.9
	requests==2.4.3
	wsgiref==0.1.2
~~~

 * At the last, you get [SAMI Python SDK](https://github.com/samsungsamiio/sami-python). Create a directory `sdk` under `sami` of the root directory of the demo app. Copy all the content of the SAMI Python SDK to `sdk` directory.

After installing all required libraries in Prerequisites, prepare demo app source code as following:

 * Create an Application in devportal.samsungsami.io:
  * The Redirect URI is set to '"http://localhost:8000/users/authorized'.
  * Choose "Client credentials, auth code" for OAuth 2.0 flow.
  * Under "PERMISSIONS", check "Read" for "Profile". 
  * Click the "Add Device Type" button. Pick a few device types to "Read" and "Write" permissions
 * Edit `python/settings.py`. Configure a few parameters at the bottom of the file. Specifically, change the value of `<YOUR CLIENT ID>` with the CLIENT ID and the value of `<YOUR CLIENT SECRET>` with the SECRET of the application just created on the Developer Portal.

After lengthy setup, now we are ready to start the django. 

 * Run the migrate command to start the db:

~~~
	$ python manage.py migrate
~~~

 * Then start the server with the command:

~~~
	$ python manage.py runserver
~~~

 * Go to your browser and access to http://localhost:8000/

Enjoy!

More about SAMI
---------------

If you are not familiar with SAMI we have extensive documentation at http://developer.samsungsami.io

The full SAMI API specification with examples can be found at http://developer.samsungsami.io/sami/api-spec.html

We blog about advanced sample applications at http://blog.samsungsami.io/

To create and manage your services and devices on SAMI visit developer portal at http://devportal.samsungsami.io

Licence and Copyright
---------------------

Licensed under the Apache License. See LICENCE.

Copyright (c) 2015 Samsung Electronics Co., Ltd.
