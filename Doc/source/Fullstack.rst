.. _Fullstack:

==========================
Working with the Fullstack
==========================

------------
Introduction
------------

While Devstack uses development web server (e.g. django), and Destack uses EdX core repositories checked out to your development host machine (and shared to the VM). The Fullstack (still VM) uses production web server (e.g. gunicorn, not django development server) and Fullstack checkes out the "production" code from EdX repositories into its VM (no development shared folders with the host machine).

You may need a Fullstack VM to test your edx-platform changes you made using Devstack, test a running course using a new edx-platform release before production deployment.

This document contains instructions for instaling the most recent named release of OpenEdX Fullstack called ``Birch``. We will install Birch Fullstack using Vagrant and Virtualbox.

For more information about ``Birch`` see `Birch release announcement <https://open.edx.org/announcements/open-edx-release-birch-release-february-24-2015>`_.

----------------------
Software Prerequisites
----------------------
Refer to :ref:`Software_Prerequisites` in Devstack section. 
   
---------------------
One-time Installation
---------------------
Fullstack Installation will require downloading a vitrual box and many repositories from edx github account. Make sure you have reliable Internet connection to be able to complete the installation steps successfully.

For a complete installation manual see `here <http://edx.readthedocs.org/projects/edx-installing-configuring-and-running/en/latest/index.html>`_. However we also provide a step by step instructions and show solutions to the common problems faced during the installation process.

Linux, MS Windows 7 (using Bash)
-----------------------------------
#. Installation should be straight forward, simply execute these commands. ::

	$ cd ~
	$ mkdir fullstack
	$ cd fullstack
	$ curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/fullstack/Vagrantfile > Vagrantfile
	$ vagrant plugin install vagrant-hostsupdater
	$ export OPENEDX_RELEASE="named-release/birch"
	$ vagrant up

MS Windows 7 (using cmd.exe)
----------------------------

#. Open Windows Command Processor which usually located in ``C:\Windows\System32\cmd.exe``.

#. Download OpenEdX ``Birch`` virtual box and prepare for provisioning step: Open CLI (cmd) with "run as administrator" (Right click the CMD program/icon and choose "Run as Administrator") ::

	C:\> mkdir fullstack
	C:\> cd fullstack
	C:\fullstack> curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/fullstack/Vagrantfile > Vagrantfile
	C:\fullstack> vagrant plugin install vagrant-hostsupdater
	C:\fullstack> SETX OPENEDX_RELEASE "named-release/birch"

#. Provisioning step: You have to open a new CLI (cmd) because SETX command we've executed in the previous step writes variables to the master environment and do not affect the current CMD session. Then execute the following command ::

	C:\fullstack> vagrant up

#. If the provisioning step didn't complete successfully you can reprovision by writing the following commands: ::

	C:\fullstack> vagrant halt
	C:\fullstack> vagrant up
	C:\fullstack> vagrant provision

.. _using_fullstack:

---------------------------
Using the OpenEdX Fullstack
---------------------------

Follow the instructions `in this wiki page <https://github.com/edx/configuration/wiki/edx-Full-stack--installation-using-Vagrant-Virtualbox>`_ to bring the VM up and start running OpenEdX Studio and LMS. In the following wiki page you will find all the instructions you need to `manage the Full stack VM <https://github.com/edx/configuration/wiki/edX-Managing-the-Full-Stack>`_. 

---------------------------------------
Deploying OpenDSAX xblocks on Fullstack
---------------------------------------

To use OpenDSAX xblocks (or any other xblock) in Fullstack Studio and LMS, there are three things you need to do:
	#) Allow All Advanced Components (first time only)
	#) Clone OpenDSAX repository inside fullstack VM.
	#) Install OpenDSAX xblocks into the virtual environment you are running the studio from.


#. To allow advanced components ssh to the VM (vagrant ssh) and do the following: ::

	$ sudo nano /edx/app/edxapp/cms.env.json
	add ("ALLOW_ALL_ADVANCED_COMPONENTS": true) under "FEATURES" attribute. Exit and save your change.

	Once the file is updated, you need to restart the services to reload the settings. 
	$ sudo /edx/bin/supervisorctl restart edxapp:

#. Before you clone the OpenDSAX repository you need to install sphinx in the VM. Refer to :ref:`toolchain` for sphinx installation command. 	

#. Clone OpenDSAX repository (inside the Fullstack VM) ::

	$ cd /edx/app/edxapp
	$ sudo -u edxapp git clone https://github.com/OpenDSA/OpenDSAX.git
	$ cd OpenDSAX
	$ sudo make pull
	$ sudo make fs-install-xblocks

	In some cases, rebooting is necessary to use the XBlock.
	$ sudo /edx/bin/supervisorctl restart edxapp:

#. Becasue OpenDSAX xblocks were developed to allow OpenDSA eBooks to be implemented in OpenEdX platform, You have to build an OpenDSA eBook first. For that sake, OpenDSAX reporsitory comes with a sample eBook called ``testX`` :: 

	$ cd /edx/app/edxapp/OpenDSAX
	$ sudo pip install -r requirements.txt
	$ sudo make fs-testX

#. To use OpenDSAX XBlocks in a course, follow the instuction `in this page <http://opendsax.readthedocs.org/en/latest/Introduction.html#trying-it-out>`_ starting from point #4.

--------------------
When things go wrong
--------------------
If you couldn't download the virtual box anything went wrong you can delete the VM and start from the begining.

#. Linux: ::

		$ vagrant halt
		$ vagrant destroy

#. MS Windows 7: ::

		C:\fullstack> vagrant halt
		C:\fullstack> vagrant destroy