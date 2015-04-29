"""This XBlock represents a multiple choice question pool. Copy most and replace the question pool html strings to use for your own questions."""

import pkg_resources
import random
import json

from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment


class BubblesortQuestionsXBlock(XBlock):
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    # maxQuestionIndex should be how many questions we have - 1
    maxQuestionIndex = Integer(help="The highest index for questions", default = 0, scope =Scope.user_state)
    # maxPoints should be changed to whatever the maximum points achievable are for this exercise
    """
    TODO:Fill in the points achievable for the exercise in the default spot.
    """
    maxPoints = Integer(help="The max points achievable for this exercise", default = 0, scope=Scope.user_state)
    

    
    score = Integer(help="Score for the exercise", default = 0, scope=Scope.user_state)

    """
    TODO: Fill in the question json files here (urls)
    """
    questionPool = ["static/json/question_template.json", "static/json/question_template.json"]

    currentQuestionIndex = Integer(help="What question we are on", default = 0, scope = Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        dat = pkg_resources.resource_string(__name__, path)
        return dat.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        
        """
        TODO: Change the value to be: How many question files there are - 1
        """
        self.maxQuestionIndex = 1;

        """
        TODO: Change the value to be what the max points achievable for this exercise is.
        """
        self.maxPoints = 20;

        self.currentQuestionIndex = random.randint(0,self.maxQuestionIndex)
        data = self.resource_string(self.questionPool[self.currentQuestionIndex])
        data = json.loads(data)
        html_context = Context({"question_title": data["question"]["problem"],
                                "max_points": self.maxPoints,
                                "score" : self.score
                                })

        """TODO: Add in html template location"""
        html_template = Template(self.resource_string("static/html/mcq_random_template.html"))

        frag = Fragment(html_template.render(html_context))
        js_context = Context({
                    "numberOfPossibleAnswers" : len(data["question"]["answers"]),
                    "answers": json.dumps(data["question"]["answers"]),
                    "solution_index": data["question"]["solution_index"]
                      })

        """TODO: Add in js resource location"""
        js_template = Template(self.resource_string("static/js/src/mcq_random_template.js"))

        js_str = js_template.render(js_context)
        frag.add_javascript(js_str)

        """TODO: add in css resource location"""
        frag.add_css(self.resource_string("static/css/mcq_random_template.css"))

        """TODO: Add in XBlocks name here"""
        frag.initialize_js('MCQRandomTemplateXBlock')
        return frag


    @XBlock.json_handler
    def getNewQuestion(self, data, suffix=''):
        tempInt = random.randint(0,self.maxQuestionIndex)
        while tempInt == self.currentQuestionIndex:
            tempInt = random.randint(0,self.maxQuestionIndex)

        self.currentQuestionIndex = tempInt
        json_data = self.resource_string(self.questionPool[self.currentQuestionIndex])
        json_data = json.loads(json_data)
        if data['question'] == 'correct' and data['flag'] == 'false':
            if self.score < self.maxPoints:
                self.score = self.score + 1
        tempQuestionArray = json_data["question"]["answers"]
        return {"question_title": json_data["question"]["problem"], "solution_index": json_data["question"]["solution_index"],"answers": tempQuestionArray,"score": self.score}

"""TODO: Replace the '<mcq_random_template/>' with your XBlock name"""
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("BubblesortQuestionsXBlock",
             """<vertical_demo>
                <mcq_random_template/>
                </vertical_demo>
             """),
        ]
"""TODO: Be sure to remove all the 'TODO' lines in this file!"""
