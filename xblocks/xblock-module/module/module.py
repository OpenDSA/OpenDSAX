"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, Integer, Float, List
from xblock.fragment import Fragment


class ModuleXBlock(XBlock):
    """
    To show student progress in all module problems in terms of total_student_score / total_weight
    """
    has_children = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    # The content controls how the Inputs attach to Graders
    def student_view(self, context=None):
        total_weight = 0
        total_student_score = 0

        result = Fragment()
        result.add_css_url(self.runtime.local_resource_url(self, 'public/css/module.css'))
        result.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/config.js'))
        result.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/module.js'))

        named_child_frags = []
        # self.children is an attribute obtained from ChildrenModelMetaclass, so disable the
        # static pylint checking warning about this.
        for child_id in self.children:  # pylint: disable=E1101
            child = self.runtime.get_block(child_id)
            total_weight += child.weight
            total_student_score += child.student_score
            frag = self.runtime.render_child(child, "student_view")
            if child.problem_type == "ss":
                self.add_ss_javascript_resources(child.problem_url, result)
            result.add_frag_resources(frag)
            named_child_frags.append(frag)

        module_completed = True if total_student_score == total_weight else False
        # Module page template
        html_template = Template(self.resource_string("public/html/student_template.html"))
        html_context = Context({"total_weight": int(total_weight), 
                                "total_student_score": int(total_student_score),
                                "module_completed": module_completed,
                                "named_children": named_child_frags,
                                }) 
        html_str = html_template.render(html_context)
        result.add_content(html_str)

        result.initialize_js('ModuleXBlock')
        return result


    def add_ss_javascript_resources(self, problem_url, fragment):
        fragment.add_javascript_url(problem_url+"../../lib/jquery.min.js")
        fragment.add_javascript_url("//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML")
        fragment.add_javascript_url(problem_url+"../../lib/jquery-ui.min.js")
        fragment.add_javascript_url(problem_url+"../../JSAV/lib/jquery.transit.js")
        fragment.add_javascript_url(problem_url+"../../JSAV/lib/raphael.js")
        fragment.add_javascript_url(problem_url+"../../JSAV/build/JSAV-min.js")
        fragment.add_javascript_url(problem_url+"../../lib/odsaUtils-min.js")
        fragment.add_javascript_url(problem_url+"../../lib/odsaMOD-min.js")
        fragment.add_javascript_url(problem_url+"../../lib/conceptMap.js")
        # <script type="text/javascript" src="_static/config.js"></script>

    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        # <jsav problem_url="http://algoviz.org/OpenDSAX/AV/Sorting/quicksortPRO.html/" required="True" threshold="0.5" long_name="" weight="100" showhide="" JXOP_fixmode="" JXOP_code="" JXOP_feedback="" JOP_lang=""></jsav>

        return [
            ("ModuleXBlock",
             """<module>
                    <jsav weight="10"></jsav>
                    <jsav weight="20"></jsav>
                    <jsav problem_type="ss" problem_url="http://opendsax.local/AV/Sorting/" short_name="quicksortCON"></jsav>
                </module>
             """),
        ]

