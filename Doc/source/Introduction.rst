.. _Introduction:

Introduction
============

OpenDSAX is the version of OpenDSA built on the OpenEdX framework.

This documentation describes various components of the OpenDSAX system.
This includes the support infrastructure for authoring OpenDSAX
xblocks and modules, information helpful for developing AVs and exercises,
documentation for the textbook configuration system (to control which
modules and exercises are generated for a specific book instance and
how the exercises are scored),
documentation for using the front-end (client-side) portion of the
logging and scoring infrastructure,
and documentation for the back-end (server-side) API and data storage
system.

AVs and exercises are typically built using the JavaScript Algorithm
Visuailzation library (JSAV).
Complete documentation for JSAV can be found at
`http://jsav.io <http://jsav.io/>`_.

If you are new to OpenDSA, it will help you to keep in mind as you
look through this manual that it targets a lot of different things,
but you are probably concerned with only one of several possible roles
at any given time.
Those roles include:

#. Content developer: Someone who wants to create or modify modules,
   visualizations, or exercises If so, you want to read the sections on
   creating content.

#. Instructor: Someone with a class to manage. If so, you want to read
   about the instructor tools. If you want to set up your own book
   instance by picking and choosing from the OpenDSA collection of
   materials, then look at compiling a book instance and the
   configuration system.

#. System administrator: Someone who wants to set up their own copy of
   OpenDSA. OpenDSA separates the front end content delivery server
   from the back end data collection server. You might want to set up
   either or both, in which case you should look at the installation
   guides.

#. OpenDSA Infrastructure developer: If you want to help to extend the
   OpenDSA infrastructure, then you will need to understand the
   details of the part of the system that you are targetting.


Trying it out
-------------

The OpenDSA project runs an OpenEdX server at ``opendsax.cc.vt.edu``.
Here is information on how you can access the server and try some
things out.

#. Point your browser to `http://opendsax.cc.vt.edu:18010 <http://opendsax.cc.vt.edu:18010>`_.

#. Register for new account and login.

#. Create a new course. Update course Schedule & Details and Grading policy.

#. To use OpenDSA XBlocks in the course: Go to Settings -> Advanced Setting sub-menu

    .. image:: _static/studio_settings.png
        :width: 205px
        :height: 198px
        :alt: alternate text
        :align: center

#. Add module, jsav and content xblocks to Advanced Module List.
       
    .. image:: _static/studio_course_advanced_settings.png
        :width: 978px
        :height: 480px
        :alt: alternate text
        :align: center

#. Go to Course Outline and create a new Section and a new subsection under it.

#. Create a new unit below the subsection and a new button "Advanced" will appear in your unit edit view.

    .. image:: _static/studio_course_unit.png
        :width: 987px
        :height: 361px
        :alt: alternate text
        :align: center

#. When you click the advanced button the following options will appear: JSAV-Based Materials, OpenDSA Content and OpenDSA Module which will allow you to add OpenDSA JSAV Materials, Contents and Modules to your courseware.
   
    .. image:: _static/studio_course_unit_xblocks.png
        :width: 997px
        :height: 423px
        :alt: alternate text
        :align: center


#. Select the OpenDSA Module option to create a new one. OpenDSA Module is a parent xblock which hosts the two other xblocks. To add jsav or content children xblocks to the Module click the "VIEW" link as shown below: 

    .. image:: _static/studio_course_unit_module_xblock.png
        :width: 997px
        :height: 483px
        :alt: alternate text
        :align: center

#. Click the Advanced button again and select OpenDSA content option. 

    .. image:: _static/studio_course_unit_content_xblock.png
        :width: 1033px
        :height: 406px
        :alt: alternate text
        :align: center

#. You can change the parameters of the Contnent xblock by pressing the edit button. Then you may change the content type and the rest of the parameters as shown below:

    .. image:: _static/studio_course_unit_content_xblock_edit.png
        :width: 924px
        :height: 527px
        :alt: alternate text
        :align: center

#. Now add JSAV-Based Materials and click Edit button to select the type of Materials that you want to include in this Module. Based on your "Problem Type" selection the second list will be populated by all avaliable Materials so far to select from. the rest of the parameters will be populated by default values based on your selected Material.

    .. image:: _static/studio_course_unit_jsav_xblock_edit.png
        :width: 905px
        :height: 516px
        :alt: alternate text
        :align: center


#. When you finish adding Contents and JSAV Materials to the Module, configuring all JSAV parameters you have to publish the Module (EdX subsection) to make it avaliable for students in the lms.

    .. image:: _static/studio_course_unit_publish.png
        :width: 1002px
        :height: 681px
        :alt: alternate text
        :align: center

#. Go to the course outline and click "View Live" button to review the Module in the EdX LMS.

#. As we mentioned that a Module is a parent for the contents and JSAV materils therefor it shows the student overall progress.
   
    .. image:: _static/lms_unit_module.png
        :width: 1273px
        :height: 448px
        :alt: alternate text
        :align: center

#. The Module calculate the total points it worth from its individual child and track student overall progress.
   
    .. image:: _static/lms_unit_PE_SS.png
        :width: 872px
        :height: 920px
        :alt: alternate text
        :align: center


