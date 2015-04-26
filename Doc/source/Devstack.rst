.. _Devstack:

=========================
Working with the Devstack
=========================

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

For more information about ``Birch`` see `Birch release announcement <https://open.edx.org/announcements/open-edx-release-birch-release-february-24-2015>`_.

----------------------
Software Prerequisites
----------------------
To install and run Devstack, you must first install the following required software.

Linux
-----
#. `VirtualBox 4.3.12 <https://www.virtualbox.org/wiki/Downloads>`_ or higher
#. `Vagrant 1.6.5 <http://www.vagrantup.com/downloads.html>`_ or higher


MS Windows 7
------------
#. `VirtualBox version 4.3.20 <http://dlc-cdn.sun.com/virtualbox/4.3.20/VirtualBox-4.3.20-96997-Win.exe>`_
#. `Vagrant version 1.6.5 <https://dl.bintray.com/mitchellh/vagrant/vagrant_1.6.5.msi>`_
#. See :ref:`curl_installation` below
   
---------------------
One-time Installation
---------------------
Devstack Installation will require downloading a vitrual box and many repositories from edx github account. Make sure you have reliable Internet connection to be able to complete the installation steps successfully.

For a complete installation manual see `here <http://edx.readthedocs.org/projects/edx-installing-configuring-and-running/en/latest/index.html>`_. However we also provide a step by step instructions and show solutions to the common problems faced during the installation process.

Linux, MS Windows 7 (using Bash)
-----------------------------------
#. Installation should be straight forward, simply execute these commands. ::

	$ cd ~
	$ mkdir devstack
	$ cd devstack
	$ curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/devstack/Vagrantfile > Vagrantfile
	$ vagrant plugin install vagrant-vbguest
	$ export OPENEDX_RELEASE="named-release/birch"
	$ vagrant up

MS Windows 7 (using cmd.exe)
----------------------------

#. Open Windows Command Processor which usually located in ``C:\Windows\System32\cmd.exe``.

#. Download OpenEdX ``Birch`` virtual box and prepare for provisioning step: Open CLI (cmd) with "run as administrator" (Right click the CMD program/icon and choose "Run as Administrator") ::

	C:\> mkdir devstack
	C:\> cd devstack
	C:\devstack> curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/devstack/Vagrantfile > Vagrantfile
	C:\devstack> vagrant plugin install vagrant-vbguest
	C:\devstack> SETX OPENEDX_RELEASE "named-release/birch"

#. Provisioning step: You have to open a new CLI (cmd) because SETX command we've executed in the previous step writes variables to the master environment and do not affect the current CMD session. Then execute the following command ::

	C:\devstack> vagrant up

#. If the provisioning step didn't complete successfully you can reprovision by writing the following commands: ::

	C:\devstack> vagrant halt
	C:\devstack> vagrant up
	C:\devstack> vagrant provision

.. _using_devstack:

--------------------------
Using the OpenEdX Devstack
--------------------------

Follow the instructions `in this wiki page <https://github.com/edx/configuration/wiki/edX-Developer-Stack#using-the-edx-devstack>`_ to bring the VM up and start running OpenEdX Studio and LMS.

--------------------------------------
Deploying OpenDSAX xblocks on Devstack
--------------------------------------

To use OpenDSAX xblocks (or any other xblock) in the Studio and LMS, there are three things you need to do:
	#) Make sure the ALLOW_ALL_ADVANCED_COMPONENTS feature flag is set to True
	#) Clone OpenDSAX repository (prefered to be inside ``devstack`` folder).
	#) Install OpenDSAX xblocks into the virtual environment you are running the studio from

Note: ALLOW_ALL_ADVANCED_COMPONENTS is set to True by default in the Devstack environment, so this part is already taken care of.

Linux
-----
#. Clone OpenDSAX repository ::

	$ cd ~/devstack
	$ git clone https://github.com/OpenDSA/OpenDSAX.git
	$ cd ~/devstack/OpenDSAX
	$ make pull

#. The easiest way to install OpenDSAX xblocks is to make OpenDSAX folder in your host machine available to the Devstack virtual machine. You can do that by adding the following line to your Vagrantfile ::

	config.vm.synced_folder "~/devstack/OpenDSAX", "/edx/OpenDSAX", create: true, nfs: true

	note: you need to put the previous line just after the following line in Vagrantfile
	config.vm.synced_folder "#{ora_mount_dir}", "/edx/app/ora/ora", create: true, nfs: true

See :ref:`both` section for remaining instructions

MS Windows 7 (using Bash)
-------------------------
#. Clone OpenDSAX repository ::

	$ cd ~/devstack
	$ git clone https://github.com/OpenDSA/OpenDSAX.git
	$ cd ~/devstack/OpenDSAX
	$ make pull

#. The easiest way to install OpenDSAX xblocks is to make OpenDSAX folder in your host machine available to the Devstack virtual machine. You can do that by adding the following line to your Vagrantfile ::

	config.vm.synced_folder "C:/path/to/devstack/OpenDSAX", "/edx/OpenDSAX", create: true, nfs: true

	note: you need to put the previous line just after the following line in Vagrantfile
	config.vm.synced_folder "#{ora_mount_dir}", "/edx/app/ora/ora", create: true, nfs: true

See :ref:`both` section for remaining instructions

.. _both:

Both
----
#. Then restart the virtual machine and SSH into it. ::

	$ vagrant halt
	$ vagrant up
	$ vagrant ssh
	note: "vagrant" is the passphrase and the password

#. Install the xblocks to the edxapp environment using pip: ::

	$ sudo su edxapp
	$ cd /edx/OpenDSAX
	$ make install-xblocks

#. Becasue OpenDSAX xblocks were developed to allow OpenDSA eBooks to be implemented in OpenEdX platform, You have to build an OpenDSA eBook first. For that sake, OpenDSAX reporsitory comes with a sample eBook called ``testX`` :: 

	$ sudo su edxapp
	$ cd /edx/OpenDSAX
	$ make ds-testX

#. Refer to :ref:`using_devstack` to start the studio and LMS::

#. To use OpenDSAX XBlocks in a course, follow the instuction `in this page <http://opendsax.readthedocs.org/en/latest/Introduction.html#trying-it-out>`_ starting from point #4.

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

In addition, this `wiki page <https://github.com/edx/configuration/wiki/Vagrant-troubleshooting>`_ shows different issues that could happen during vagrant installation and how to solve them.

.. _curl_installation:

----------------------------------
cURL installation for MS Windows 7
----------------------------------

On the curl `download <http://curl.haxx.se/download.html>`_  
page there's a link to the download `wizard <http://curl.haxx.se/dlwiz/>`_
Complete all the steps as following:

curl executable  > Win64  > Generic  > Any  > x86_64
you will end up in `this page <http://www.confusedbycode.com/curl/>`_ download (With Administrator Privileges (free)) verion.

-----------------------------------------
Developing and testing XBlock on Devstack
-----------------------------------------

Once you install your XBlocks into Devstack, any changes or updates you 
do to the XBlock will be automatically loaded by Devstack when you refresh the browser. 
So you only need to keep Devstack up and running while you are developing and testing your XBlock.