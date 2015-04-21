"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from django.template import Context, Template

from lms_mixin import LmsCompatibilityMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin, StudioContainerXBlockMixin
from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, Integer, Float, List
from xblock.fragment import Fragment


class ModuleXBlock(XBlock, LmsCompatibilityMixin, StudioEditableXBlockMixin, StudioContainerXBlockMixin):
    """
    To show student progress in all module problems in terms of total_student_score / total_weight
    """
    has_children = True

    display_module = Boolean(
        help = "Whether the module is diplayed or not:",
        default = True,
        scope = Scope.settings)

    short_name = String(
        help = "Module Short Name:",
        default = "Quicksort",
        scope = Scope.settings)

    long_name = String(
        help = "Module Long Name:",
        default = "Quicksort",
        scope = Scope.settings)

    # TODO: provide a list of available chapters
    chapter = String(
        help = "Chapter name",
        default = "Sorting",
        scope = Scope.settings)

    editable_fields = ('chapter', 'long_name', 'short_name')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    def student_view(self, context=None):
        total_weight = 0
        total_student_score = 0

        result = Fragment()
        result.add_css_url(self.runtime.local_resource_url(self, 'public/css/main.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/_static/haiku.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/_static/pygments.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/normalize.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/JSAV/css/JSAV.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/odsaMOD-min.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/jquery-ui.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/lib/odsaStyle.css'))
        # result.add_css_url(self.runtime.local_resource_url(self, 'public/css/module.css'))
        self.add_javascript_resources(result)
        result.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/student_view.js'))

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
        html_template = Template(self.resource_string("public/html/student_view.html"))
        html_context = Context({"total_weight": int(total_weight), 
                                "total_student_score": int(total_student_score),
                                "module_completed": module_completed,
                                "named_children": named_child_frags,
                                "correct_icon": self.runtime.local_resource_url(self, 'public/images/correct-icon.png'),
                                "incorrect_icon": self.runtime.local_resource_url(self, 'public/images/incorrect-icon.png'),
                                }) 
        html_str = html_template.render(html_context)
        result.add_content(html_str)
        result.initialize_js('ModuleXBlock')
        return result


    def author_preview_view(self, context):
        result = Fragment()
        children_names = []
        for child_id in self.children:  # pylint: disable=E1101
            child = self.runtime.get_block(child_id)
            children_names.append(child.long_name)

        html_template = Template(self.resource_string("public/html/author_preview_view.html"))
        html_context = Context({"children_names": children_names}) 
        html_str = html_template.render(html_context)
        result.add_content(html_str)
        return result


    def author_edit_view(self, context):
        """
        Child blocks can override this to control the view shown to authors in Studio when
        editing this block's children.
        """
        fragment = Fragment()
        fragment.add_css_url(self.runtime.local_resource_url(self, 'public/css/main.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/_static/haiku.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/_static/pygments.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/lib/normalize.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/JSAV/css/JSAV.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/lib/odsaMOD-min.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/lib/jquery-ui.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/lib/odsaStyle.css'))
        # fragment.add_css_url(self.runtime.local_resource_url(self, 'public/css/module.css'))
        self.add_javascript_resources(fragment)
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/student_view.js'))

        self.render_children(context, fragment, can_reorder=True, can_add=True)
        fragment.initialize_js('ModuleXBlock')
        return fragment


    @XBlock.json_handler
    def change_problem(self, data, suffix=''):
        # if 'display_module' in data:
        #     self.display_module = data['display_module']
        if 'moduleShortName' in data:
            self.short_name = data['moduleShortName']
        if 'moduleLongName' in data:
            self.long_name = data['moduleLongName']


    def add_javascript_resources(self, fragment):
        # fragment.add_resource_url(self.runtime.local_resource_url(self, 'public/js/src/x-mathjax-config.js'), 'text/x-mathjax-config', placement="head")
        js_template = Template(self.resource_string("public/js/src/config.js"))
        js_context = Context({'displayModule': self.display_module,
                              'shortName': self.short_name,
                              'longName': self.long_name,
                              'chapter': self.chapter})
        js_str = js_template.render(js_context)
        fragment.add_javascript(js_str)
        # fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/jquery.min.js'))
        # fragment.add_javascript_url("//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML")
        # fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/jquery-ui.min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/JSAV/lib/jquery.transit.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/JSAV/lib/raphael.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/JSAV/build/JSAV-min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/odsaUtils-min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/odsaMOD-min.js'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/lib/conceptMap.js'))
    
    @XBlock.json_handler
    def storeLogData(self, data, suffix=''):
        event_list = []
        for e in data.values():
            event = e.replace("\\", "")
            self.runtime.publish(self, "event", event)
            event_list.append(event)
        return event_list

    # workbench while developing your XBlock.
        # <content short_name="Quicksort"/>
        # <jsav problem_type="ss" problem_url="/AV/Sorting/" short_name="quicksortCON"></jsav>
        # <jsav problem_type="pe" problem_url="/AV/Sorting/" problem_width="802" problem_height="422" required="True" threshold="0.5" short_name="quicksortPRO" long_name="Quick Sort" weight="100" showhide="hide" JXOP_fixmode="fix" JXOP_code="none" JXOP_feedback="continuous" JOP_lang="en"></jsav>
        # <jsav problem_type="pe" problem_url="/AV/Sorting/" problem_width="822" problem_height="452" required="True" threshold="0.5" short_name="quicksortAV" long_name="Quick Sort" weight="100" showhide="hide" JXOP_fixmode="fix" JXOP_code="none" JXOP_feedback="continuous" JOP_lang="en"></jsav>
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ModuleXBlock",
             """<module>
                    <content short_name="Quicksort"/>
                    <jsav problem_type="ss" problem_url="/AV/Sorting/" short_name="quicksortCON"></jsav>
                    <jsav problem_type="pe" problem_url="/AV/Sorting/" problem_width="805" problem_height="515" required="True" threshold="0.5" short_name="quicksortPRO" long_name="Quick Sort" weight="100" showhide="hide" JXOP_fixmode="fix" JXOP_code="none" JXOP_feedback="continuous" JOP_lang="en"></jsav>
                </module>
             """),
        ]

