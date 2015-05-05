How to configure readthedocs.org
================================

In order to use ``sphinx.ext.autodoc`` extension you have to have all the dependencies of OpenDSAX XBlocks installed in the environment that you run sphinx form, to achive that in readthedocs.org you need to enable the virtualenv feature in the Admin page, which will install OpenDSAX project into a virtualenv, and allow to specify a requirements.txt file for it.


Build the documentation offline
===============================

Since OpenDSAX XBlocks dependencies are XBlock and Django packages, you can/should activate SDK virtualenv and build the documentaion inside it


Documentation
-------------

  * [architecture](doc/worldmap-xblock-arch.rst) - An overview of how everything goes together.
  * [user-documentation](doc/worldmap-xblock-doc.rst) - A user-level document describing how to create a worldmap-based edX "unit"
  * [setting up AWS](doc/aws-setup.txt) - How to set up an Amazon AWS instance of edX with the worldmap plugin working.
  * [development environment](doc/dev_configure.rst) - How to setup a development environment.
  * [Notes on LTI migration](doc/worldmap-connector-migration-to-LTI-notes.rst) - ideas on migrating to LTI




The trick is to give the virtualenv in which you build your docs access to 
the global site-packages directory -- see Advanced Settings > Use system 
packages. RTD has numpy 1.8 and scipy installed system wide.

As for testing, to ensure that you can build your docs from scratch in 
a new virtualenv (each version of the docs gets its own virtualenv), try 
deleting the build environment:
http://read-the-docs.readthedocs.org/en/latest/builds.html#deleting-a-stale-or-broken-build-environment