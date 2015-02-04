import pkg_resources
import json, urllib2

from django.template import Context, Template

from lms_mixin import LmsCompatibilityMixin
from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean,Integer,Float, List
from xblock.fragment import Fragment


class JSAVXBlock(XBlock, LmsCompatibilityMixin):
    instructions = String(
        help = "The instructions to show to learners",
        default = "Write instructions to learners here...",
        scope = Scope.settings)
    
    problem_url = String(
        help = "Url of the jsav exercise",
        default = "http://opendsa.local/AV/Sorting/quicksortPRO.html",
        scope = Scope.settings)

    student_score = Float(
        help = "student's score on this problem",
        values = {"min": 0, "step": 0.1},
        default = 0,
        scope = Scope.user_state)

    student_submissions = List(
        help="Student's stored submissions",
        default = [],
        scope = Scope.user_state)

    def student_view(self, context):
        html = self.resource_string('public/html/example.html')
        fragment = Fragment(html.format(self=self))

        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/example.js'))
        fragment.add_css(self.runtime.local_resource_url(self, 'public/css/jsav_xblock.css'))
        fragment.initialize_js('JSAVXBlock')
        return fragment

    def studio_view(self, context):
        template = Template(self.resource_string("public/html/studio.html"))
        exercise_information = json.load(urllib2.urlopen("https://trak.cs.hut.fi/jsav/jsondump"))
        context = Context({"exercises": exercise_information, "problem_url": self.problem_url, "points": self.points})
        fragment = Fragment(template.render(context))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/studio.js'))
        fragment.initialize_js("JSAVXBlockStudioEdit")
        return fragment

    @XBlock.json_handler
    def change_problem(self, data, suffix=''):
        if 'problem_url' in data:
            self.problem_url = data['problem_url']
        if 'points' in data:
            self.points = float(data['points'])

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    @XBlock.json_handler
    def report_progress(self, data, suffix=''):
        if "score" in data.keys():
            max_score = float(data["score"]["correct"]) / float(data["score"]["total"]) * self.max_score()
            submission = { 'score' : data.get("score", None),
                           'seed' : data.get("seed", None), 
                           'log': data.get("log", None),
                           'datetime': data.get("datetime", None) }
            self.student_submissions.append(submission)
            if max_score == self.max_score():
                self.student_score = max_score
                self.runtime.publish(self, "grade", { "value": self.student_score, "max_value": self.max_score() } )
        return {"student_score": self.student_score}


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("JSAVXblock",
             """<vertical_demo>
                <jsav />
                </vertical_demo>
             """),
        ]