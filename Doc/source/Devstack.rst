.. _Devstack:

==============================
Working with the devstack
==============================

This section provides complete instructions for 
setting up the complete devstack.

-----------------------------------------
What is devstack and why you may need it?
-----------------------------------------

EdX Devstack is your tool for developing and testing Open edX on your local computer. Devstack is a Vagrant instance that uses the same system requirements as a production system.

Devstack includes the following edX components:

The edX Learning Management System (LMS)
EdX Studio, for course development
Forums
Open Response Assessments
Devstack Simplifies certain production settings to make development more convenient. For example, nginx and gunicorn are disabled in Devstack; Devstack uses Django’s runserver instead.

To run Devstack, you must install VirtualBox 4.3.12 or greater, and Vagrant 1.6.5 or greater. (See MS Windows 7 section for Windows users)

- See more at: http://open.edx.org/devstack#sthash.wPyaOINX.dpuf


------------
Installation 
------------

MS Windows 7
============

#. follow the steps here
#. Install Virtual box version 4.3.20.
#. Install Vagrant version 1.6.5.
#. if you run into symlinks problem discussed here 
#. And to solve the symlinks issue I followed Edx/Configiraton wiki solution here.
#. if that didn't work then try symlinks issue solved by following 


I ran into this same problem. My solution was pretty straight forward.  It's Oct. 2014 now, and I'm using the latest Vagrant.  To overcome this error I had to open a CLI (cmd) with "run as administrator".  Thats right click the CMD program/icon and choose "Run as Administrator".  This is necessary to allow Vagrant to create teh symlinks.  BEFORE running Vagrant set:  VAGRANT_USE_VBOXFS=true.  Thats:

  C:>  set VAGRANT_USE_VBOXFS=true

You'll need this since Windows 8+ does not have the NFS client available unless you have the enterprise version available, so you have to instruction Vagrant to not use NFS; hence the environment variable.

Once I got past this coffee-script issue (Node.js) I ran into a Python install problem.  This you can get over using the instructions at: 
 https://github.com/edx/configuration/wiki/edX-Developer-Stack#installing-the-edx-developer-stack


Two useful posts discussing edX devstack installation problems on Windows here and here


---------------------------
Install xblocks in devstack 
---------------------------



-------------
named release 
-------------


---------------------------------------
Installing the Open edX Developer Stack
---------------------------------------

from documentation (where is the documentation)

---------------------------------------
Knowledge background
---------------------------------------


- Introduction (birch, takes long time, background information)
- tools chain (cURL)
- One time installation (run as administrator)
	- setx env-var named-release
	- Installation validation
	- what about ports forwarding and shared folders issue.
	- the provisiong setp should be completed sucessfully, use provision option to reprovision the
- troubles on windows
	- symlinks
	- coffe scipt generation
	- if connection to github is inturrepted use vagrant up, vagrant provision
- run devstack
- LMS work flow
- Studio work flow
- install OpenDSAX xblocks on dev stack
- managing devstack (working with devstack) provision
- When things go wrong
- remove the devstack




run as administrator 
install curl