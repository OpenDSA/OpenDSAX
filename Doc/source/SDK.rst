.. _SDK:

====================
Working with the SDK
====================

For most developers, your primary task will be creating xblocks.
So you need a way to test that an xblock that you create does work.
The simplest way to do this is to set up the xblock SDK.

Basic instructions for setting up the SDK are available at the
xblock-sdk project's GitHub repository
(see https://github.com/edx/xblock-sdk).
However, below are detailed instructions for getting this set up under
Linux or MS Windows.

-----
Linux
-----
#. Install Python 2.7. ::

	$ sudo apt-get install python

#. Install git. ::

	$ sudo apt-get install git

#. Install pip. ::

	$ sudo apt-get install python-pip

#. Install virtualenv. ::

	$ sudo pip install virtualenv

#. Create the following two directories ::

	$ mkdir ~/envs
	$ mkdir ~/dev

#. Create and activate a new virtualenv. ::

	$ cd ~/envs
	$ virtualenv sdk

	If you have multiple verisons of python installed, use python 2.7 to create the new virtualenv.

	$ which python
	/path/to/python2.7
	$ virtualenv -p /path/to/python2.7 sdk

	$ . ~/envs/sdk/bin/activate


#. Clone repo: https://github.com/edx/xblock-sdk. ::

	(sdk) $ cd ~/dev
	(sdk) $ git clone https://github.com/edx/xblock-sdk.git

#. Install your version of xblock-sdk. (you need to run these commands while sdk vitrualenv is active) ::

   (sdk) $ cd ~/dev/xblock-sdk
   (sdk) $ sudo make install

#. If you encounterd a problem with libxml, you may need to install: ::

	(sdk) $ sudo apt-get install libxml2-dev libxslt1-dev

#. Run the django development server ::

	(sdk) $ sudo python manage.py runserver

#. You should be able to visit http://127.0.0.1:8000/ and see something like this:

	.. image:: _static/workbench_home.png
	   :width: 752px
	   :height: 427px
	   :alt: alternate text
	   :align: center

#. Start creating your new xblock. ::

	$ cd ~/dev
	$ git clone https://github.com/OpenDSA/OpenDSAX.git
	$ cd OpenDSAX/xblocks
	$ mkdir test
	$ cd test
	$ python ~/dev/xblock-sdk/script/startnew.py
	short name: test
	Class name: TestXBlock

#. You will need to register your xblock (entry point) in order to be able to see it in workbench (sdk). 
	create the file requirements.txt in test folder to allow to register the package ::
	
	-e .

#. Then run pip to register the test xblock package and allow XBlock to find the entry point (in sdk virtualenv) ::

	(sdk) $ cd ~/dev/OpenDSAX/xblocks/test
	(sdk) $ sudo pip install -r requiements.txt

#. Now (re)start the workbench server.
   
#. You should be able to visit http://127.0.0.1:8000/ and see your new xblock TestXBlock in the list

	.. image:: _static/workbench_test_XBlock.png
		:width: 650px
		:height: 488px
		:alt: alternate text
		:align: center

#. If anything was worng for any reason, remove ``~/envs/sdk`` folder and restart from the begining.

------------
MS Windows 7
------------

#. We assume that you have installed Git (see http://git-scm.com/download/win), and that you have access to a command line-based interface. We recommend that Bash command line interface that comes with the GitHub installation.

#. **Note for Bash CLI users:** After you install Python, pip and virtualenv you can install workbench using Bash CLI by following the exact same steps described in Linux section (without sudo), and use the activate command path on windows as ``~/envs/sdk/Scripts/activate`` not ``~/envs/sdk/bin/activate``.

**Installtion steps using Windows command Processor:**

#. Install Python 2.7. (see https://www.python.org/downloads/)

#. Install pip. (see https://pip.pypa.io/en/latest/installing.html)

#. Open Windows Command Processor which usually located in ``C:\Windows\System32\cmd.exe``.

#. Install virtualenv. ::
   
	C:\>pip install virtualenv

#. Create the following two directories ::

	C:\>mkdir envs
	C:\>mkdir dev

#. Create and activate a new virtualenv. ::

	C:\>cd envs
	C:\envs>virtualenv sdk
	C:\envs>sdk\Scripts\activate.bat
	(sdk) C:\envs>

#. Clone repo: https://github.com/edx/xblock-sdk. ::

	(sdk) C:\>cd dev
	(sdk) C:\dev>git clone https://github.com/edx/xblock-sdk.git

#. Install your version of xblock-sdk. (you need to run these commands while sdk vitrualenv is active) ::

	(sdk) C:\>cd dev\xblock-sdk
	(sdk) C:\dev\xblock-sdk>make install

#. If you run into a problem regarding a missing ``vcvaralls.bat`` file, then go to http://www.microsoft.com/en-us/download/details.aspx?id=44266 and install that version of the Microsoft Visual C++ compiler. Then repeat the ``make install`` command again.

#. Run the django development server ::

	(sdk) C:\dev\xblock-sdk>python manage.py runserver

#. You should be able to visit http://127.0.0.1:8000/ and see something like this:

	.. image:: _static/workbench_home.png
	   :width: 752px
	   :height: 427px
	   :alt: alternate text
	   :align: center


#. Start creating your new xblock. ::

	C:\>cd dev
	C:\dev>git clone https://github.com/OpenDSA/OpenDSAX.git
	C:\dev>cd OpenDSAX\xblocks
	C:\dev\OpenDSAX\xblocks>mkdir test
	C:\dev\OpenDSAX\xblocks>cd test
	C:\dev\OpenDSAX\xblocks\test>python c:\dev\xblock-sdk\script\startnew.py
	short name: test
	Class name: TestXBlock

#. You will need to register your xblock (entry point) in order to be able to see it in workbench (sdk). 
	create the file requirements.txt in test folder to allow to register the package ::
	
	-e .

#. Then run pip to register the test xblock package and allow XBlock to find the entry point (in sdk virtualenv) ::

	(sdk) C:\>cd dev\OpenDSAX\xblocks\test
	(sdk) C:\dev\OpenDSAX\xblocks\test>pip install -r requiements.txt

#. Now (re)start the workbench server.
   
#. You should be able to visit http://127.0.0.1:8000/ and see your new xblock TestXBlock in the list

	.. image:: _static/workbench_test_XBlock.png
		:width: 650px
		:height: 488px
		:alt: alternate text
		:align: center

#. If anything was worng for any reason, remove ``C:\envs\sdk`` folder and restart from the begining.

--------------------------
Rerun workbench web server
--------------------------
#. Once you have the workbench installed and you want to rerun it, you have to activate sdk virtualenv first then run the web server. 

	#. Linux ::

		$ . ~/envs/sdk/bin/activate
		(sdk) $ cd ~/dev/xblock-sdk
	 	(sdk) $ sudo python manage.py runserver

	#. MS Windows 7 ::

		C:\>envs\sdk\Scripts\activate.bat
		(sdk) C:\>cd dev\xblock-sdk
		(sdk) C:\dev\xblock-sdk>python manage.py runserver

-----------------------------
Developing and testing xblock
-----------------------------

Once you install your XBlock into sdk virtualenv, the workbench will automatically display its scenarios for you to experiment with. Any changes or updates you do to the xblock will be automatically loaded by the workbench when you refresh the browser. So you only need to keep your workbench up and running while you are developing your xblock.
