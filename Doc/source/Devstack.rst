.. _Devstack:

=========================
Working with the Devstack
=========================

This section provides complete instructions for setting up OpenEdX Devstack.

------------
Introduction
------------
OpenEdX Devstack is your tool for developing and testing OpenEdX on your local computer. Devstack is a Vagrant instance that uses the same system requirements as a production system.

The Devstack instance is designed to run code and tests, but you can do most development in the host environment:

* Git repositories are shared with the host system, so you can use your preferred text editor/IDE.
* You can load pages served by the running Vagrant instance.

The Devstack configuration has the following components:

* LMS (student facing website)
* Studio (course authoring)
* Forums / elasticsearch / ruby (discussion forums)
* ORA (Open Response Assessor)

This document contains instructions for instaling the most recent named release of OpenEdX Devstack called ``Birch``.

For more information on ``Birch`` see `Birch release announcement <https://open.edx.org/announcements/open-edx-release-birch-release-february-24-2015>`_.

----------------------
Software Prerequisites
----------------------
To install and run Devstack, you must first install the following required software.

#. Linux:
     #) `VirtualBox 4.3.12 <https://www.virtualbox.org/wiki/Downloads>`_ or higher
     #) `Vagrant 1.6.5 <http://www.vagrantup.com/downloads.html>`_ or higher

#. MS Windows 7:
     #) `VirtualBox version 4.3.20 <http://dlc-cdn.sun.com/virtualbox/4.3.20/VirtualBox-4.3.20-96997-Win.exe>`_
     #) `Vagrant version 1.6.5 <https://dl.bintray.com/mitchellh/vagrant/vagrant_1.6.5.msi>`_
     #) See below for installing cURL on windows


---------------------
One-time Installation
---------------------
Devstack Installation will require downloading a vitrual box and many repositories from edx github account. Make sure you have reliable Internet connection to be able to complete the installation steps successfully.

For a complete installation manual see `here <http://edx.readthedocs.org/projects/edx-installing-configuring-and-running/en/latest/index.html>`_. However we also provide a step by step instructions and show solutions to the most common problems faced during the installation process.

In addition, this `wiki page <https://github.com/edx/configuration/wiki/Vagrant-troubleshooting>`_ shows different issues that could happen during vagrant installation and how to solve them.


Linux
-----
#. Installation should be straight forward, simply execute these commands. ::

	$ cd ~
	$ mkdir devstack
	$ cd devstack
	$ curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/devstack/Vagrantfile > Vagrantfile
	$ vagrant plugin install vagrant-vbguest
	$ export OPENEDX_RELEASE="named-release/birch"
	$ vagrant up

[TODO] MS Windows (using Bash) 
------------------------------

MS Window 7
-----------

#. Download OpenEdX ``Birch`` virtual box and prepare for provisioning step: Open CLI (cmd) with "run as administrator" (Right click the CMD program/icon and choose "Run as Administrator") ::

	C:\> mkdir devstack
	C:\> cd devstack
	C:\devstack> curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/devstack/Vagrantfile > Vagrantfile
	C:\devstack> vagrant plugin install vagrant-vbguest
	C:\devstack> SETX OPENEDX_RELEASE "named-release/birch"

2- Provisioning step: You have to open a new CLI (cmd) because SETX command we've executed in the previous step writes variables to the master environment in the registry, edits will only take effect when a new command window is opened - they do not affect the current CMD or PowerShell session. Then execute the following command. ::

	C:\devstack> vagrant up

3- If the provisioning step didn't complete successfully you can reprovision by writing the following commands: ::

	C:\devstack> vagrant halt
	C:\devstack> vagrant up
	C:\devstack> vagrant provision

--------------------------
Using the OpenEdX devstack
--------------------------

Follow the instructions `On this wiki page <https://github.com/edx/configuration/wiki/edX-Developer-Stack#lms-workflow>`_ to bring the VM up and start running OpenEdX LMS and Studio.

------------------------------------
Deploying OpenDSAX xblocks on devstack
------------------------------------

#. To use OpenDSAX xblocks (or any other xblocks) in the Studio and LMS, there are three things you need to do:
	#) Clone OpenDSAX repository (prefered to be inside devstack folder).
	#) Make sure the ALLOW_ALL_ADVANCED_COMPONENTS feature flag is set to True
	#) Install OpenDSAX xblocks into the virtual environment you are running the studio from

#. This is how you can do these steps:
	#) Clone OpenDSAX repository
		#. Linux ::

			$ cd ~
			$ git clone https://github.com/OpenDSA/OpenDSAX.git
			$ cd OpenDSAX
			$ make pull

		#. MS Wiindows 7 ::

			C:\> cd devstack
			C:\devstack> git clone https://github.com/OpenDSA/OpenDSAX.git
			C:\devstack> cd OpenDSAX
			C:\devstack\OpenDSAX> make pull

	#) ALLOW_ALL_ADVANCED_COMPONENTS is set to True by default in the devstack environment, so this part is already taken care of.
	#) The easiest way to install OpenDSAX xblocks is to make OpenDSAX folder available to the devstack machine. You can do that by adding the following lines to your Vagrantfile:

		#. Linux ::

			config.vm.synced_folder "/path/to/OpenDSAX", "/edx/OpenDSAX", create: true, nfs: true

		#. MS Windows 7 ::

			config.vm.synced_folder "C:/path/to/OpenDSAX", "/edx/OpenDSAX", create: true, nfs: true

#. Then restart the machine and SSH into it. ::

	$ vagrant halt
	$ vagrant up
	$ vagrant ssh
	note: "vagrant" is the passphrase and the password

#. Becasue OpenDSAX xblocks were developed to allow OpenDSA eBooks to be implemented in 
OpenEdX platform, You have to build an OpenDSA ebook first. For that sake, OpenDSAX 
reporsitory comes with a sample eBook called ``testX`` ::

	$ sudo su edxapp
	$ cd /edx/OpenDSAX
	$ make testXEDX	

#. Install the xblocks to the edxapp environment using pip: ::

	$ sudo su edxapp
	$ cd /edx/OpenDSAX
	$ pip install -r requirements.txt
	$ cd /edx/xblocks/xblock-module
	$ pip install -r requirements.txt
	$ cd /edx/xblocks/xblock-jsav
	$ pip install -r requirements.txt
	$ cd /edx/xblocks/xblock-content
	$ pip install -r requirements.txt

#. Start the studio ::

	$ cd /edx/app/edxapp/edx-platform
	$ paver devstack studio

#. follow the instuction `here <http://opendsax.readthedocs.org/en/latest/Introduction.html#trying-it-out>`_ starting from point #4.

--------------------
When things go wrong
--------------------
If you couldn't download the virtual box or the provisioing step did't finish or 
anything went wrong you can delete the VM and start from the begining.

#. Linux: ::

		$ vagrant halt
		$ vagrant destroy

#. MS Windows 7: ::

		C:\devstack> vagrant halt
		C:\devstack> vagrant destroy


---------------------------------
cURL installation for MS Window 7
---------------------------------

On the curl `download <http://curl.haxx.se/download.html>`_  
page there's a link to the download `wizard <http://curl.haxx.se/dlwiz/>`_
Complete all the steps as follows:

executable  > Win64  > Generic  > *  > x86_64 (http://www.confusedbycode.com/curl/) download (With Administrator Privileges (free))

executable  > Win32  > Generic  > *  > i386 (Download WITH SUPPORT SSL) 

Finally, you can copy curl.exe into %windir% and it should become available on the command line.