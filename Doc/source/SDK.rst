.. _SDK:

Working with the SDK
====================

For most developers, your primary task will be creating xblocks.
So you need a way to test that an xblock that you create does work.
The simplest way to do this is to set up the SDK.

Basic instructions for setting up the SDK:
(see https://github.com/edx/xblock-sdk).

#. Install Python 2.7.

#. Install pip.

#. Clone repo: https://github.com/edx/xblock-sdk

#. Install virtualenv. (NEED DIRECTIONS FOR THIS.)

#. Activate the virtualenv.

#. Go to your version of xblock-sdk.

#. Do:

   ``make install``


Now you are ready to test your work.

#. Do:

   ``python manage.py runserver``

   This will start up the web server.

#. Open a web browser to: http://127.0.0.1:8000
