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

When a Module XBlock is loaded into LMS it will contain one or more JSAV
XBlocks. Each client side JavaScript of JSAV XBlock will trigger events as
student starts to interact with it. Depends on the JSAV XBlock instance type,
events might be "message" events (which are triggered by IFramed profieciency
exercises and AVs) or "jsav-log-event" events (which are triggered by slide
shows). Module XBlock client side JavaScript will listen for these events and
handle them, scoring events will be filtered and validated before Module
XBlock calls 'reportProgress' function of the correspoding JSAV XBlock in
order to report the score back to JSAV XBlock server side via AJAX request.
Server side can have more evaluation rules than the client side, Actually only
server side can decide whether the student will be awarded profeciency and
given the problem points or not. Server side decision will be sent back via
AJAX response and JSAV and Module XBlocks client side will update proficiency
and score indicator(s) based on server response.

Here below a sequance diagram that present interactions happening between
Module and JSAV XBlocks and between client and server sides as well.

    .. figure:: _static/OpenDSAX-SeqDiagram.svg
       :scale: 100%
       :alt: OpenDSAX XBlocks interactions.
       :align: center    

       Fig 2: OpenDSAX XBlocks sequence diagram.


.. list-table:: suggested subtopics
   :widths: 800
   :header-rows: 1

   * - Subtopics
   * - XBlocks interaction with EdX
   * - Scoring (About grades and grade book)
   * - Code layout
   * - Restrictions and limitations
   * - Ongoing work
   * - How to contribute
   * - Nice to have: ``Programming detail hints``