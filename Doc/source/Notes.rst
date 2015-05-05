.. _Notes:

=========================
Developer's Notes
=========================

In OpenDSAX, user interactions with interactive content (i.e slideshows, AVs, and exercises) are logged and saved on the EDX server as native EDX events using the platform's ``publish`` method. The event logging process is completely invisible to the content developer, and he is not required to add anything to his code. However for interested developers, the logged events can be accessed as follows:

* From the browser, you can simply investigate the localStorage object from the browser's console by typing ``localStorage``. This object will contain all the logged user interactions that are not yet saved on the server.

* From the EDX platform, you can access user interactions after being saved on the server by accessing the ``tracking.log`` file on the vagrant machine. The path to the ``traking.log`` file is ::

	vagrant@precise64:/edx/var/log/tracking$