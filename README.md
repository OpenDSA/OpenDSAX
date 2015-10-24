OpenDSAX
========

NOTE: THIS REPOSITORY IS OBSOLETE.

Development repository for a (now aborted) OpenDSA implementation within
theOpenEdX framework. We dicided to go with LTI, and the various
traditional LMS that support LTI, instead of OpenEdX.

It was meant to explore the possibility for replacing the existing
OpenDSA infrastructure (which is mostly home grown) with one built on
the OpenEdX framework.
The idea is to preserve most of the existing content development
system (based on RST with iframe'ed visualizations and exercises), but
replace the entire scoring server and necessary components of the
client-side infrastructure libraries.

## Setup

To check out a read-only copy of this repository:

    git clone git://github.com/OpenDSAX/OpenDSAX.git OpenDSAX

To check out a read-write copy of this repository
(requires permission to commit to the repo):

    git clone https://YOURGITHUBID@github.com/OpenDSA/OpenDSAX.git OpenDSAX

Once you have cloned this repository, you will need to initialize and
update the submodules and compile some of the libraries.
Do the following:

    git submodule init
    make pull

In order to pull a more recent copy of JSAV than what is in the submodule:

    cd JSAV
    git pull https://github.com/vkaravir/JSAV
