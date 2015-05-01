from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, Integer, Float, List
from xblock.fragment import Fragment
from xblock.exceptions import JsonHandlerError
from xblock.validation import Validation
import pkg_resources
import json
import urllib2
import inspect
import random
import string  # pylint: disable=W0402
import time
import logging

from django.template import Context, Template

from lms_mixin import LmsCompatibilityMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin, StudioContainerXBlockMixin


class JSAVXBlock(XBlock, LmsCompatibilityMixin,
                 StudioEditableXBlockMixin, StudioContainerXBlockMixin):

    """JSAVXBlock is responsible for showing all the OpenDSA interactive materials types 
    like slide shows, Algorithm Visualizations and Proficiency exercises that were developed
    using JSAV library. 

    JSAVXBlock will allow instructors to choose the type of the materials to show and based
    on the type chosen the JSAVXblock will show all available materials related to that type.

    Once the instructor selects one specific material, all the default configuration parameters for this material
    will be loaded by default into JSAVXblock instance, and still the instructor can change these default values 
    before creating an instance of the JSAVXblock.
    """
    XBlock_type = String(
        help="The XBlock type",
        scope=Scope.content,
        default="problem")

    seed = Integer(
        help="Random seed for this student",
        scope=Scope.user_state,
        default=0)

    instructions = String(
        help="The instructions to show to learners",
        default="Write instructions to learners here...",
        scope=Scope.settings)

    problem_type = String(
        help="whether slideshow 'ss' or proficiency exercise 'pe'",
        default="pe",
        values=({"value": "pe", "display_name": "Proficiency Exercise"},
                {"value": "ss", "display_name": "Slide Show"},
                {"value": "av", "display_name": "Algorithm Visualization"}
                ),
        scope = Scope.settings)

    # TODO: provide a list of available problems
    problem_url = String(
        help="URL of the JSAV-Based exercise",
        default="/AV/Sorting/",
        scope=Scope.settings)

    problem_width = Integer(
        help="width",
        default=825,
        values={"min": 100, "max": 1000, "step": 1},
        scope=Scope.settings)

    problem_height = Integer(
        help="height",
        default=600,
        values={"min": 100, "max": 1000, "step": 1},
        scope=Scope.settings)

    required = Boolean(
        help="Whether the exercise is required for module proficiency",
        default=False,
        scope=Scope.settings)

    threshold = Float(
        display_name="Percentage For Proficiency",
        help="the percentage a student needs to score on the exercise to obtain proficiency, defaults to 100% (1 on a 0-1 scale)",
        values={"min": 0, "max": 10, "step": 0.1},
        default=0.5,
        scope=Scope.settings)

    long_name = String(
        display_name="Long Name",
        help="Problem Long Name",
        default="quickSort",
        scope=Scope.settings,)

    short_name = String(
        help="Problem short Name",
        default="quicksortPRO",
        scope=Scope.settings)

    js_resources = String(
        help="supplementary js files",
        default="quicksortCODE.js",
        scope=Scope.settings)

    AVAILABLE_PROBLEMS = {
        'login': {
            'html': "static/html/login.html",
            'css': ["static/css/sqli.css"],
            'js': ["static/js/src/login.js"],
            'js_objs': ['SqlInjectionXBlock'],
            'log': 'previous_answers_login',
        },
        'union': {
            'html': "static/html/union.html",
            'css': ["static/css/sqli.css"],
            'js': [],
            'js_objs': [],
            'log': 'previous_answers_union',
        },
    }

    showhide = String(
        help="controls whether or not the exercises is displayed and a Show / Hide button created",
        default="show",
        values=({"value": "hide", "display_name": "Hide"},
                {"value": "show", "display_name": "Show"}),
        scope = Scope.settings)

    JXOP_fixmode = String(
        help="JSAV Exercise Option - fixmode",
        default="fix",
        # values = ({"value":"fix","display_name":"Fix"}, {"value":"undo","display_name":"Undo"}),
        scope=Scope.settings)

    JXOP_code = String(
        help="JSAV Exercise Option - code",
        default="none",
        # values = ({"value":"none","display_name":"None"}, {"value":"processing","display_name":"Processing"}),
        scope=Scope.settings)

    JXOP_feedback = String(
        help="JSAV Exercise Option - feedback",
        default="continuous",
        scope=Scope.settings)

    JOP_lang = String(
        help="JSAV configration Option - lang",
        default="en",
        # values = ({"value":"en","display_name":"English"},
        #           {"value":"fi","display_name":"Finnish"},
        #           {"value":"fr","display_name":"French"},
        #           {"value":"pt","display_name":"Portuguese"},
        #           {"value":"sv","display_name":"Swedish"}),
        scope=Scope.settings)

    student_score = Float(
        help="student's score on this problem",
        values={"min": 0, "step": 0.1},
        default=0,
        scope=Scope.user_state)

    student_proficiency = Boolean(
        help="whether student achived the problem proficiency",
        default=False,
        scope=Scope.user_state)

    student_submissions_pe = List(
        help="Student's stored submissions for pe",
        default=[],
        scope=Scope.user_state)

    student_submissions_ss = List(
        help="Student's stored submissions for ss",
        default=[],
        scope=Scope.user_state)

    editable_fields = ('problem_type', 'short_name', 'problem_url', 'problem_width',
                       'problem_height', 'required', 'threshold', 'long_name', 'js_resources',
                       'showhide', 'JXOP_fixmode', 'JXOP_code', 'JXOP_feedback',
                       'JOP_lang', 'display_name', 'weight')

    def student_view(self, context):
        html_context = Context({"student_score": self.student_score,
                                "name": self.short_name,
                                "weight": self.weight,
                                "width": self.problem_width,
                                "height": self.problem_height,
                                "problem_url": self.get_problem_url(self.short_name + ".html"),
                                "student_proficiency": self.student_proficiency,
                                "correct_icon": self.runtime.local_resource_url(self, 'public/images/correct-icon.png'),
                                "incorrect_icon": self.runtime.local_resource_url(self, 'public/images/incorrect-icon.png'),
                                })
        if self.problem_type == "ss":
            html_template = Template(
                self.resource_string("public/html/ss_student_view.html"))
            fragment = Fragment(html_template.render(html_context))
            # if self.js_resources:
            #     js_resources = json.loads(self.js_resources)["js"]
            #     for js_file in js_resources:
            #         fragment.add_javascript_url(self.get_problem_url(js_file))
            if self.js_resources:
                fragment.add_javascript_url(
                    self.get_problem_url(self.js_resources))
            fragment.add_javascript_url(
                self.get_problem_url(self.short_name + ".js"))
            fragment.add_css_url(
                self.get_problem_url(self.short_name + ".css"))
        else:
            html_template = Template(
                self.resource_string("public/html/student_view.html"))
            fragment = Fragment(html_template.render(html_context))

        js_template = Template(
            self.resource_string("public/js/student_view.js"))
        js_context = Context({"seed": self.seed if self.seed else self.set_student_seed(),
                              "shortName": self.short_name,
                              "longName": self.long_name,
                              "points": self.weight,
                              "required": self.required,
                              "threshold": self.threshold,
                              "problemType": self.problem_type,
                              })

        js_str = js_template.render(js_context)
        fragment.add_javascript(js_str)
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/css/jsav_xblock.css'))
        fragment.initialize_js('JSAVXBlock' + '_' + str(self.seed))
        return fragment

    def studio_view(self, context):
        fragment = super(JSAVXBlock, self).studio_view(context, override=True)
        # fragment = Fragment()
        jsav_based_info = json.load(urllib2.urlopen(
            "http://algoviz.org/OpenDSAX/AV/jsav_based_materials_list.json"))

        # Test trying to render the list of PE the same way utils lib is
        # rendering fields
        html_template2 = Template(
            self.resource_string("public/html/studio_view_jsav_based_materials.html"))
        html_context2 = Context({"pe": jsav_based_info["pe"], "av": jsav_based_info[
                                "av"], "ss": jsav_based_info["ss"]})
        html_str2 = html_template2.render(html_context2)
        fragment.add_content(html_str2)
        # fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/studio_view_jsav_based_materials.js'))

        fragment.add_javascript_url(
            self.runtime.local_resource_url(self, 'public/js/studio_edit_jsav.js'))
        fragment.initialize_js('StudioEditableXBlockJSAV')
        return fragment

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def set_student_seed(self):
        """Set a random seed for the student so they each have different but repeatable data."""
        # Don't return zero, that's the default, and the sign that we should
        # make a new seed.
        self.seed = int(time.time() * 1000) % 100 + 1
        return self.seed

    def get_problem_url(self, short_name):
        """Handy helper for getting URL plus pearamters."""
        # workbench version
        base_url = 'public' + self.problem_url + short_name
        # lms version
        # base_url = "/xblock/resource/jsav/public"
        # URL = base_url+self.problem_url+self.short_name

        URL = self.runtime.local_resource_url(self, base_url)
        if self.problem_type == "pe":
            URL += "?" + "JXOP-fixmode" + "=" + self.JXOP_fixmode + "&"\
                + "JXOP-code" + "=" + self.JXOP_code + "&"\
                + "JXOP-feedback" + "=" + self.JXOP_feedback + "&"\
                + "JOP-lang" + "=" + self.JOP_lang + "&"\
                + "seed" + "=" + \
                str(self.seed if self.seed else self.set_student_seed())
        return URL

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

    @XBlock.json_handler
    def report_progress(self, data, suffix=''):
        already_proficient = self.student_proficiency if self.student_proficiency else False
        if self.problem_type in ("ss", "av"):
            self.student_proficiency = True
            self.student_score = self.weight
            self.runtime.publish(
                self, "grade", {"value": self.student_score, "max_value": self.weight})
        else:
            if "score" in data.keys():
                current_score = float(
                    data["score"]["correct"]) / float(data["score"]["total"])
                submission = {'score': data.get("score", None),
                              'seed': data.get("seed", None),
                              'log': data.get("log", None),
                              'datetime': data.get("datetime", None)}
                self.student_submissions_pe.append(submission)
                if current_score >= self.threshold:
                    self.student_proficiency = True
                    self.student_score = self.weight
                    self.runtime.publish(
                        self, "grade", {"value": self.student_score, "max_value": self.weight})
        return {"student_score": self.student_score,
                "problem_weight": self.weight,
                "student_proficiency": self.student_proficiency,
                "already_proficient": already_proficient,
                "correct_icon": self.runtime.local_resource_url(self, 'public/images/correct-icon.png'),
                "incorrect_icon": self.runtime.local_resource_url(self, 'public/images/incorrect-icon.png')}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        # The XBLock can be initialized with parameters by using the following syntax
        # <jsav short_name="quicksortPRO"></jsav>
        return [
            ("JSAVXblock",
             """<vertical_demo>
                    <jsav problem_type="pe" problem_url="/AV/Sorting/" required="True" threshold="0.5" short_name="quicksortPRO" long_name="Quick Sort" weight="100" showhide="hide" JXOP_fixmode="fix" JXOP_code="none" JXOP_feedback="continuous" JOP_lang="en"></jsav>
                </vertical_demo>
             """),
        ]
