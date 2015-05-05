.. _Architecture:

=============================================
OpenDSAX XBlocks Architecture (Draft Version)
=============================================

------------
Introduction
------------
XBlock is component architecture for building courseware. An XBlock is similar in structure to web application “plugin” and fills a similar niche. The OpenDSAX XBlocks attempts to host `OpenDSA <http://algoviz.org/OpenDSA/>`_ eBooks into EdX XBlock architecture.

In this release we provide the following functionality:

#. Display of JSAV-based proficiency exercises, Algorithm Visualizations and slide shows.
#. Studio user interface to allow course author to select from a list of available exercises
#. Course authors can define exercise weight as well as other excursive configurations
#. Student score tracking by the exercise XBlock and module XBlock as well.
#. Student interaction and event tracking logging.


---------------
Main Components
---------------

OpenDSAX XBlock architecture consists of three XBlocks Module, JSAV and
Content. Module XBlock is the parent XBlock and it serves as a container to
the other two XBlocks, it provides JavaScript and CSS resources to its
children. It is considered also as the centralized place in which JSAV score
events and logging events are checked and validated. Module XBlock receives
score and logging events from children XBlocks though messaging.

Messaging facility is built on top of HTML5’s cross-document messaging via
`Window.postMessage <https://developer.mozilla.org/en-
US/docs/Web/API/Window/postMessage>`_ capabilities which lets a main page
communicate with a page loaded within an IFrame and vice versa. This
technology is working on all current versions of all major browsers as
enumerated `here <http://caniuse.com/#feat=x-doc-messaging>`_. Below diagram
shows the main components for each XBlock.

    .. figure:: _static/OpenDSAX-XBlocks-highlevel.svg
       :scale: 100%
       :alt: OpenDSAX XBlocks main components.
       :align: center    

       Fig 1: OpenDSAX XBlocks main components.

------------
How it works
------------

When a Module XBlock is loaded into EdX LMS it will contain one or more JSAV XBlock. Each client side javascript of JSAV XBlock will trigger events as student starts to interact with it. Events might contains scoring or logging data. JSAV XBlock will trigger the a message event in case of profieciency exercises and algorithem visualization because these  ...

"""Problem XBlock, and friends.

These implement a general mechanism for problems containing input fields
and checkers, wired together in interesting ways.

This code is in the XBlock layer.

A rough sequence diagram::

      BROWSER (Javascript)                 SERVER (Python)

    Problem    Input     Checker          Problem    Input    Checker
       |         |          |                |         |         |
       | submit()|          |                |         |         |
       +-------->|          |                |         |         |
       |<--------+  submit()|                |         |         |
       +------------------->|                |         |         |
       |<-------------------+                |         |         |
       |         |          |     "check"    |         |         |
       +------------------------------------>| submit()|         |
       |         |          |                +-------->|         |
       |         |          |                |<--------+  check()|
       |         |          |                +------------------>|
       |         |          |                |<------------------|
       |<------------------------------------+         |         |
       | handleSubmit()     |                |         |         |
       +-------->| handleCheck()             |         |         |
       +------------------->|                |         |         |
       |         |          |                |         |         |

"""


.. list-table::
   :widths: 800
   :header-rows: 1

   * - Subtopics
   * - XBlocks interaction with each other (activity diagram/ sequence diagram)
   * - XBlocks interaction with EdX
   * - Scoring
   * - About grades and grade book
   * - Code layout
   * - Restrictions and limitations
   * - On going work
   * - How to contribute
   * - Nice to have: ``Programming detail hints``
