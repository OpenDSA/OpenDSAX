.. _ExerciseQuestions:

=========================
Creating new questions
=========================

------------
Introduction
------------
An instance of a question xblock takes a json file, and displays questions to the user. In order to add new questions to OpenDSAX, a few steps are required.

------------
Structure
------------
Each instance of the question xblock will look at one particular summary question file. This file contains the names and locations of all the individual questions that belong to it.

------------
Creating a question
------------
To create a new question, look at the existing questions in the json/individualQuestion/ folder for the syntax to follow. A few things to know:

* If your question requires any jsav drawing, make sure you add a field usesJsav = true. You'll also then need to insert your jsav code into the field jsavStuff = "<your code>". IMPORTANT!!! JSON does not support multi line strings, and will add \n characters to your code. keep it all on one line.
* If no jsav is required, set usesJsav = false.

------------
Adding to a summary question
------------
To add an additional, individual question to the summary question, you just need to open up the summary question file, and insert the new string into the array of questions. You must also increment the numQuestionsForExercise field (Could perhaps get rid of this and use length of the question array?)

------------
Adding a summary question
------------
If no summary question exists that represents your question, you'll need to create a new file inside the summary question directory of the question xblock.
Each summary question requires these fields:

* cssString: This is the location of the css file for the question (could perhaps not and hardcode this?)
* htmlString: This is the location of the html file for the question (could perhaps not and hardcode this?)
* jsString: This is the location of the javascript file for the question (could perhaps not and hardcode this?)
* maxPointsForExercise: How many points does a student need to complete this exercise?
* numQuestionsForExercise: How many questions the exercise has
* questionUrls: This is an array that contains the strings of each question in the form of their URL

=========================
Using in the Workbench
=========================
To test or use your questions in the workbench, you'll need to first install the questions xblock to your sdk:

* From in the xblock directory, run 'pip install -e questions'
* Open the question.py file in the question directory
* At the bottom, there is the workbench scenario. Change the summary question file attribute to be the one you wish to see on the workbench.