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

    display_module = Boolean(
        help = "",
        default = True,
        scope = Scope.settings)

    short_name = String(
        help = "",
        default = "QuicksortCOMP1",
        scope = Scope.settings)

    long_name = String(
        help = "",
        default = "Quicksort",
        scope = Scope.settings)

    chapter = String(
        help = "",
        default = "Sorting",
        scope = Scope.settings)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    # The content controls how the Inputs attach to Graders
    def student_view(self, context=None):
        total_weight = 0
        total_student_score = 0

        result = Fragment()
        result.add_css_url(self.runtime.local_resource_url(self, 'public/_static/pygments.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/_static/haiku.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/css/module.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/normalize.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/JSAV/css/JSAV.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/odsaMOD-min.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/jquery-ui.css'))
        result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/odsaStyle.css'))
        result.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/module.js'))
        self.add_javascript_resources(result)

        named_child_frags = []
        # self.children is an attribute obtained from ChildrenModelMetaclass, so disable the
        # static pylint checking warning about this.
        for child_id in self.children:  # pylint: disable=E1101
            child = self.runtime.get_block(child_id)
            if child.XBlock_type == "problem":
                total_weight += child.weight
                total_student_score += child.student_score
            frag = self.runtime.render_child(child, "student_view")
            # if child.problem_type == "ss":
            #     self.add_javascript_resources(child.problem_url, result)
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


    def add_javascript_resources(self, fragment):
        js_template = Template(self.resource_string("public/js/src/config.js"))
        js_context = Context({
                              'displayModule': self.display_module,
                              'shortName': self.short_name,
                              'longName': self.long_name,
                              'chapter': self.chapter,
                            }) 
        js_str = js_template.render(js_context)
        fragment.add_resource_url(self.runtime.local_resource_url(self, 'public/js/src/x-mathjax-config.js'), 'text/x-mathjax-config', placement="head")
        fragment.add_javascript(js_str)
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/jquery.min.js'))
        fragment.add_javascript_url("//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML")
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/jquery-ui.min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/JSAV/lib/jquery.transit.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/JSAV/lib/raphael.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/JSAV/build/JSAV-min.js'))

        # fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/config.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/odsaUtils-min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/odsaMOD-min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/conceptMap.js'))
        # <script type="text/javascript" src="_static/config.js"></script>

    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ModuleXBlock",
             """<module>
                    <content/>
                    <jsav weight="20"></jsav>
                    <jsav problem_type="ss" problem_url="/AV/Sorting/" short_name="quicksortCON"></jsav>
                    <jsav problem_type="pe" problem_url="/AV/Sorting/" required="True" threshold="0.5" short_name="quicksortPRO" long_name="Quick Sort" weight="100" showhide="hide" JXOP_fixmode="fix" JXOP_code="none" JXOP_feedback="continuous" JOP_lang="en"></jsav>
                </module>
             """),
        ]

