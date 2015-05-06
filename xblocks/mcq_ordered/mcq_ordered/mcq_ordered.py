"""This XBlock represents a multiple choice question pool. Copy most and replace the question pool html strings to use for your own questions."""

import pkg_resources
import random
import json

from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment


class MCQOrderedXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    # maxQuestionIndex should be how many questions we have - 1
    maxQuestionIndex = Integer(help="The highest index for questions", default = 0, scope =Scope.user_state)
    # maxPoints should be changed to whatever the maximum points achievable are for this exercise
    maxPoints = Integer(help="The max points achievable for this exercise", default = 0, scope=Scope.user_state)
    
    score = Integer(help="Score for the exercise", default = 0, scope=Scope.user_state)

    """
    Fill in the question html files here (urls)
    """
    questionPool = ["static/html/bubblesort_Question1.html"]
    currentQuestionIndex = Integer(help="What question we are on", default = 0, scope = Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):

        """
        Here we need to get a random file from the pool of html strings.
        We can declare an array of html strings, and get an index and random.
        Should we inject the header/score html code prior to the random question?
        """

        json_data = json.load(self.resource_string(self.questionPool[currentQuestionIndex]))

        self.maxQuestionIndex = json_data["num_questions"]
        self.maxPoints = json_data["max_points"]
        html_context = Context({"question_title": json_data["question"].problem,
                                "max_points": self.maxPoints
                                })

        questionString = self.questionPool[self.currentQuestionIndex]

        html_template = Template(self.resource_string("static/html/bubblesort_Question1.html"))
        frag = Fragment(html_template.render(html_context))
        frag.add_css(self.resource_string("static/css/bubblesortquestions.css"))
        frag.add_javascript(self.resource_string("static/js/src/bubblesortquestions.js"))
        frag.initialize_js('BubblesortQuestionsXBlock')
        return frag

    problem_view = student_view


    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def getNewQuestion(self, data, suffix=''):

        self.currentQuestionIndex += 1
        questionString = self.questionPool[self.currentQuestionIndex]

        newHTML = self.resource_string(questionString)
        if data['question'] == 'correct' and data['flag'] == 'false':
            if self.score < self.maxPoints:
                self.score = self.score + 1
        return {"html": newHTML, "score": self.score}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("BubblesortQuestionsXBlock",
             """<vertical_demo>
                <mcq_ordered/>
                </vertical_demo>
             """),
        ]
