"""This XBlock represents a multiple choice question pool. Copy most and replace the question pool html strings to use for your own questions."""

import pkg_resources
import random
import json

from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment


class MCQRandomTemplateXBlock(XBlock):
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    # maxQuestionIndex should be how many questions we have - 1
    maxQuestionIndex = Integer(help="The highest index for questions", default = 0, scope =Scope.user_state)
    # maxPoints should be changed to whatever the maximum points achievable are for this exercise
    maxPoints = Integer(help="The max points achievable for this exercise", default = 20, scope=Scope.user_state)
    

    
    score = Integer(help="Score for the exercise", default = 0, scope=Scope.user_state)

    """
    Fill in the question json files here (urls)
    """
    questionPool = ["test_Question1.json"]
    currentQuestionIndex = Integer(help="What question we are on", default = 0, scope = Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        dat = pkg_resources.resource_string(__name__, path)
        return dat.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):

        self.currentQuestionIndex = random.randint(0,self.maxQuestionIndex)
        data = self.resource_string(self.questionPool[self.currentQuestionIndex])
        data = json.loads(data)
        html_context = Context({"question_title": data["question"]["problem"],
                                "max_points": self.maxPoints,
                                "score" : self.score
                                })
        html_template = Template(self.resource_string("static/html/bubblesort_Question1.html"))
        frag = Fragment(html_template.render(html_context))
        js_context = Context({
                    "numberOfPossibleAnswers" : len(data["question"]["answers"]),
                    "answers": json.dumps(data["question"]["answers"]),
                    "solution_index": data["question"]["solution_index"]
                      })
        js_template = Template(self.resource_string("static/js/src/mcq_random_template.js"))
        js_str = js_template.render(js_context)
        frag.add_javascript(js_str)
        frag.add_css(self.resource_string("static/css/mcq_random_template.css"))
        frag.initialize_js('MCQRandomTemplateXBlock')
        return frag


    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def getNewQuestion(self, data, suffix=''):

        tempInt = random.randint(0,self.maxQuestionIndex)
        if self.maxQuestionIndex > 0:
            while tempInt == self.currentQuestionIndex:
                tempInt = random.randint(0,self.maxQuestionIndex)

        self.currentQuestionIndex = tempInt

        json_data = self.resource_string(self.questionPool[self.currentQuestionIndex])
        json_data = json.loads(data)
        if data['question'] == 'correct' and data['flag'] == 'false':
            if self.score < self.maxPoints:
                self.score = self.score + 1
        tempQuestionArray = json_data["question"]["answers"]


        return {"question_title": json_data["question"]["problem"], "answers" : "tempQuestionArray", "score": self.score}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
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
