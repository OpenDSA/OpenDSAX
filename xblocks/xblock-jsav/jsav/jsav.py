import pkg_resources
import json, urllib2

from django.template import Context, Template

from lms_mixin import LmsCompatibilityMixin
from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, Integer, Float, List
from xblock.fragment import Fragment


class JSAVXBlock(XBlock, LmsCompatibilityMixin):
    instructions = String(
        help = "The instructions to show to learners",
        default = "Write instructions to learners here...",
        scope = Scope.settings)
    
    problem_url = String(
        help = "URL of the JSAV-Based exercise",
        default = "http://algoviz.org/OpenDSAX/AV/Sorting/quicksortPRO.html",
        scope = Scope.settings)

    required = Boolean(
        help = "Whether the exercise is required for module proficiency",
        default = False,
        scope = Scope.settings)

    threshold = Float(
        display_name="Percentage For Proficiency",
        help = "the percentage a student needs to score on the exercise to obtain proficiency, defaults to 100% (1 on a 0-1 scale)",
        values = {"min": 0, "step": 0.1},
        default = 0.9,
        scope = Scope.settings)

    long_name = String(
        help = "Problem Long Name",
        default = "",
        scope = Scope.settings)

    showhide = String(
        help = "controls whether or not the exercises is displayed and a Show / Hide button created",
        default = "hide",
        scope = Scope.settings)

    JXOP_fixmode = String(
        help = "JSAV Exercise Option - fixmode",
        default = "fix",
        scope = Scope.settings)

    JXOP_code = String(
        help = "JSAV Exercise Option - code",
        default = "none",
        scope = Scope.settings)

    JXOP_feedback = String(
        help = "JSAV Exercise Option - feedback",
        default = "continuous",
        scope = Scope.settings)

    JOP_lang = String(
        help = "JSAV configration Option - lang",
        default = "en",
        scope = Scope.settings)

    student_score = Float(
        help = "student's score on this problem",
        values = {"min": 0, "step": 0.1},
        default = 0,
        scope = Scope.user_state)
 
    student_proficiency = Boolean(
        help = "whether student achived the problem proficiency",
        default = False,
        scope = Scope.user_state)

    student_submissions = List(
        help="Student's stored submissions",
        default = [],
        scope = Scope.user_state)

    def student_view(self, context):
        template = Template(self.resource_string("public/html/student_view.html"))
        context = Context({"student_score": self.student_score, 
                           "weight": self.weight, 
                           "problem_url": self.get_problem_url(), 
                           "student_proficiency": self.student_proficiency})

        fragment = Fragment(template.render(context))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/student_view.js'))
        fragment.add_css_url(self.runtime.local_resource_url(self, 'public/css/jsav_xblock.css'))
        fragment.initialize_js('JSAVXBlock')
        return fragment

    def studio_view(self, context):
        template = Template(self.resource_string("public/html/studio.html"))
        exercise_information = json.load(urllib2.urlopen("https://trak.cs.hut.fi/jsav/jsondump"))
        context = Context({"exercises": exercise_information, 
                           "problem_url": self.get_problem_url(), 
                           "points": self.weight,
                           "required": self.required,
                           "threshold":self.threshold})

        fragment = Fragment(template.render(context))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/studio.js'))
        fragment.initialize_js("JSAVXBlockStudioEdit")
        return fragment

    @XBlock.json_handler
    def change_problem(self, data, suffix=''):
        if 'problem_url' in data:
            self.problem_url = data['problem_url']
        if 'weight' in data:
            self.weight = float(data['weight'])
        if 'threshold' in data:
            self.threshold = float(data['threshold'])
        if 'required' in data:
            self.required = float(data['required'])

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def get_problem_url(self):
        """Handy helper for getting URL plus paramters."""
        URL = self.problem_url+"?"+"JXOP-fixmode"+"="+self.JXOP_fixmode+"&"+"JXOP-code"+"="+self.JXOP_code+"&"+"JXOP-feedback"+"="+self.JXOP_feedback+"&"+"JOP-lang"+"="+self.JOP_lang
        return URL

    @XBlock.json_handler
    def report_progress(self, data, suffix=''):
        if "score" in data.keys():
            current_score = float(data["score"]["correct"]) / float(data["score"]["total"])
            submission = { 'score' : data.get("score", None),
                           'seed' : data.get("seed", None), 
                           'log': data.get("log", None),
                           'datetime': data.get("datetime", None) }
            self.student_submissions.append(submission)
            if current_score >= self.threshold:
                self.student_proficiency = True
                self.student_score = self.max_score()
                self.runtime.publish(self, "grade", { "value": self.student_score, "max_value": self.max_score() } )
        return {"student_score": self.student_score,
                "student_proficiency": self.student_proficiency}


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        # The XBLock can be initialized with parameters by using the following syntax
        # <jsav problem_url="http://algoviz.org/OpenDSAX/AV/Sorting/quicksortPRO.html/" required="True" threshold="0.5" long_name="" weight="100" showhide="" JXOP_fixmode="" JXOP_code="" JXOP_feedback="" JOP_lang=""></jsav>
        return [
            ("JSAVXblock",
             """<vertical_demo>
                    <jsav></jsav> 
                </vertical_demo>
             """),
        ]