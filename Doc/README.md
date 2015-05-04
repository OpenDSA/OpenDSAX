How to configure readthedocs.org
================================

In order to use ``sphinx.ext.autodoc`` extension you have to have all the
dependencies of OpenDSAX XBlocks installed in the environment in which you run
sphinx, to achieve that in readthedocs.org you need to enable the virtualenv
feature in the Admin page, which will install OpenDSAX project into a
virtualenv, and allow to specify a requirements.txt file for it.


Build the documentation offline
===============================

Since OpenDSAX XBlocks dependencies are XBlock and Django packages, thankfully
these packages are installed in SDK virtualenv. So you should activate SDK
virtualenv and build the documentation inside it.