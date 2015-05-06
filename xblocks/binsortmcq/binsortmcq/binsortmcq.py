import pkg_resources
import random
import json

from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String
from xblock.fragment import Fragment


class BinSortMCQXBlock(XBlock):
    summaryQuestion = String(help="", default = "", scope = Scope.user_state)
    maxQuestionIndex = Integer(help="The highest index for questions", default = 0, scope =Scope.user_state)
    maxPoints = Integer(help="The max points achievable for this exercise", default = 10, scope=Scope.user_state)
    score = Integer(help="Score for the exercise", default = 0, scope=Scope.user_state)
    questionPool = List(default = [])
    currentQuestionIndex = Integer(help="What question we are on", default = 0, scope = Scope.user_state)
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        dat = pkg_resources.resource_string(__name__, path)
        return dat.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        print(self.summaryQuestion)
        questionData = self.resource_string(self.summaryQuestion)
        questionData = json.loads(questionData)
        self.maxQuestionIndex = questionData["numQuestionsForExercise"] - 1;        
        self.maxPoints = questionData["maxPointsForExercise"];                
        self.currentQuestionIndex = random.randint(0,self.maxQuestionIndex)

        self.questionPool = questionData["questionUrls"][:]
        data = self.resource_string(self.questionPool[self.currentQuestionIndex])
        data = json.loads(data)
        html_context = Context({"question_title": data["question"]["problem"],
                                "max_points": self.maxPoints,
                                "score" : self.score
                                })
        html_template = Template(self.resource_string(questionData["htmlString"]))

        frag = Fragment(html_template.render(html_context))
        js_context = Context({
                    "numberOfPossibleAnswers" : len(data["question"]["answers"]),
                    "answers": json.dumps(data["question"]["answers"]),
                    "jsavStuff": data["jsavStuff"],                    
                    "solution_index": data["question"]["solution_index"]
                      })
        js_template = Template(self.resource_string(questionData["jsString"]))

        js_str = js_template.render(js_context)
        frag.add_javascript(js_str)
        frag.add_css(self.resource_string(questionData["cssString"]))
        frag.initialize_js(questionData["xblockName"])
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

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("BinSortMCQXBlock",
             """<vertical_demo>
                <binsortmcq summaryQuestion="static/json/questionInfo.json"></binsortmcq>
                </vertical_demo>
             """),
        ]
