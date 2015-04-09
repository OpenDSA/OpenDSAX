.. _SDK:

====================
Working with the SDK
====================

For most OpenDSAX developers, your primary task will be creating
xblocks.
So you need a way to test that an xblock that you create does work.
The simplest way to do this is to set up the xblock SDK.

Basic instructions for setting up the SDK are available at the
xblock-sdk project's GitHub repository
(see https://github.com/edx/xblock-sdk).
However, below are detailed instructions for getting this set up under
Linux or MS Windows.

------------------------
Setting up the toolchain
------------------------

The first step is to make sure that you have the tools that you need
for the actual installation, and for doing work later.

Linux
=====

Install what you don't already have of Python 2.7, git, pip, and
virtualenv. ::

   $ sudo apt-get install python
   $ sudo apt-get install git
   $ sudo apt-get install python-pip
   $ sudo pip install virtualenv

MS Windows 7
============

#. Install Git (see http://git-scm.com/download/win)

#. Install Python 2.7. (see https://www.python.org/downloads/)

#. Install pip. (see https://pip.pypa.io/en/latest/installing.html)

#. Install virtualenv. From a command line interface. ::

      C:\> pip install virtualenv


---------------------
One-time Installation
---------------------

Now you need to initialize your virtual environment, install the SDK,
and the OpenDSX repositories.

If anything goes wrong for any reason, remove the ``~/envs/sdk`` folder
and restart from the beginning.


Linux, MacOS
============

#. Create the following two directories ::

      $ mkdir ~/envs
      $ mkdir ~/dev

#. Create and activate a new virtualenv. We are going to call it
   "sdk", but really you could use any name that you like.::

      First find where your version of python 2.7 is installed.

      $ which python
      /path/to/python2.7

      Now you create your virtual environment for use later.

      $ virtualenv -p /path/to/python2.7 sdk

#. Clone the two repositories. ::

   $ cd ~/dev
   $ git clone https://github.com/edx/xblock-sdk.git
   $ git clone https://github.com/OpenDSA/OpenDSAX.git

#. Now you are ready to initialize your version of xblock-sdk. You
   need to run these commands while the sdk vitrualenv is active. ::

      $ . ~/envs/sdk/bin/activate
      (sdk) $ cd ~/dev/xblock-sdk
      (sdk) $ sudo make install

#. If you encountered a problem with libxml, you may need to install
   it, and then retry ``make install``. ::

      (sdk) $ sudo apt-get install libxml2-dev libxslt1-dev

MS Windows (using Bash)
=======================

#. Open your Bash shell window.

#. Create the following two directories. ::

      $ mkdir ~/envs
      $ mkdir ~/dev

#. Create and activate a new virtualenv. We are going to call it
   "sdk", but really you could use any name that you like. ::

      First find where your version of python 2.7 is installed.

      $ which python
      /path/to/python2.7

      Now you create your virtual environment for use later.

      $ virtualenv -p /path/to/python2.7 sdk

#. Clone the two repositories. ::

      $ cd ~/dev
      $ git clone https://github.com/edx/xblock-sdk.git
      $ git clone https://github.com/OpenDSA/OpenDSAX.git

#. Now you are ready to initialize your version of xblock-sdk. You
   need to run these commands while the sdk vitrualenv is active. ::

      $ . ~/envs/sdk/Scripts/activate
      (sdk) $ cd ~/dev/xblock-sdk
      (sdk) $ make install

#. If you encountered a problem with libxml, you may need to install
   it, and then retry ``make install``. ::

      (sdk) $ sudo apt-get install libxml2-dev libxslt1-dev

#. If you run into a problem regarding a missing ``vcvaralls.bat``
   file, then go to
   http://www.microsoft.com/en-us/download/details.aspx?id=44266 and
   install that version of the Microsoft Visual C++ compiler. Then
   repeat the ``make install`` command again.


MS Windows (using cmd.exe)
==========================

#. Open Windows Command Processor which usually located in
   ``C:\Windows\System32\cmd.exe``.

#. Create the following two directories ::

      C:\> cd c:\
      C:\> mkdir envs
      C:\> mkdir dev

#. Create and activate a new virtualenv. ::

      C:\> cd envs
      C::\envs> virtualenv sdk
      C:\envs> sdk\Scripts\activate.bat

#. Now you are ready to initialize your version of xblock-sdk. You
   need to run these commands while the sdk vitrualenv is active. ::

      (sdk) $ cd ~/dev/xblock-sdk
      (sdk) $ make install

#. If you run into a problem regarding a missing ``vcvaralls.bat``
   file, then go to
   http://www.microsoft.com/en-us/download/details.aspx?id=44266 and
   install that version of the Microsoft Visual C++ compiler. Then
   repeat the ``make install`` command again.


----------------------------
Run the workbench web server
----------------------------

Anytime that you want to run the SDK workbench, you have to activate
your virtual environment, and then the python web server.
Note that if you just did the installation steps above, then you
aready have a virtual environment activated.

#. Linux, MacOS, MS Windows 7 (Bash) ::

      $ . ~/envs/sdk/bin/activate
      (sdk) $ cd ~/dev/xblock-sdk
      (sdk) $ sudo python manage.py runserver

#. MS Windows 7 (cmd.exe) ::

      C:\> envs\sdk\Scripts\activate.bat
      (sdk) C:\> cd dev\xblock-sdk
      (sdk) C:\dev\xblock-sdk> python manage.py runserver


--------------------------
Try out the sample XBlocks
--------------------------

You should be able to visit http://127.0.0.1:8000/ and see something like this:

   .. image:: _static/workbench_home.png
      :width: 752px
      :height: 427px
      :alt: alternate text
      :align: center


-------------------
Create a new xblock
-------------------
#. Linux

   #. Create a new xblock using a template-based generator for new XBlocks ::

         $ cd ~/dev/OpenDSAX/xblocks
         $ mkdir test
         $ cd test
         $ python ~/dev/xblock-sdk/script/startnew.py
         short name: test
         Class name: TestXBlock

   #. Then create the file requirements.txt in test folder to allow to
      register the package, as well as automatically install other
      dependencies that your xblock might need.

   #. For the test xblock you need to write only one line ``-e .`` in
      requirements.txt. The ``-e .`` option tells to always use the
      latest files from the development directory, instead of
      packaging the files when you run the command.

   #. Then run pip to register the test xblock package and allow
      XBlock to find the entry point (in sdk virtualenv) ::

         (sdk) $ cd ~/dev/OpenDSAX/xblocks/test
         (sdk) $ sudo pip install -r requiements.txt

   #. Now (re)start the workbench server.
	   
   #. You should be able to visit http://127.0.0.1:8000/ and see your
      new xblock TestXBlock in the list

         .. image:: _static/workbench_test_XBlock.png
            :width: 650px
            :height: 488px
            :alt: alternate text
            :align: center

#. Windows

   #. Create a new xblock using a template-based generator for new XBlocks ::

         C:\> cd dev\OpenDSAX\xblocks
         C:\dev\OpenDSAX\xblocks> mkdir test
         C:\dev\OpenDSAX\xblocks>cd test
         C:\dev\OpenDSAX\xblocks\test>python c:\dev\xblock-sdk\script\startnew.py
         short name: test
         Class name: TestXBlock

   #. Then create the file requirements.txt in test folder to allow to
      register the package, as well as automatically install other
      dependencies that your xblock might need:

#. For the test xblock you need to write only one line ``-e .`` in
   requirements.txt. the ``-e .`` option tells to always use the
   latest files from the development directory, instead of packaging
   the files when you run the command.

#. Then run pip to register the test xblock package and allow XBlock
   to find the entry point (in sdk virtualenv) ::

      (sdk) C:\>cd dev\OpenDSAX\xblocks\test
      (sdk) C:\dev\OpenDSAX\xblocks\test>pip install -r requiements.txt

#. Now (re)start the workbench server.
	   
#. You should be able to visit http://127.0.0.1:8000/ and see your new
   xblock TestXBlock in the list

      .. image:: _static/workbench_test_XBlock.png
         :width: 650px
         :height: 488px
         :alt: alternate text
         :align: center


-----------------------------
Developing and testing xblock
-----------------------------

Once you install your XBlock into sdk virtualenv, the workbench will
automatically display its scenarios for you to experiment with. Any
changes or updates you do to the xblock will be automatically loaded
by the workbench when you refresh the browser. So you only need to
keep your workbench up and running while you are developing your
xblock.
