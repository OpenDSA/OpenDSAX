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
        named_child_frags = []
        # self.children is an attribute obtained from ChildrenModelMetaclass, so disable the
        # static pylint checking warning about this.
        for child_id in self.children:  # pylint: disable=E1101
            child = self.runtime.get_block(child_id)
            total_weight += child.weight
            total_student_score += child.student_score
            frag = self.runtime.render_child(child, "student_view")
            result.add_frag_resources(frag)
            named_child_frags.append(frag)
        result.add_css("""
            .module {
                border: solid 1px #888; padding: 3px;
            }
            """)
        module_completed = True if total_student_score == total_weight else False
        context = Context({"total_weight": int(total_weight), 
                           "total_student_score": int(total_student_score),
                           "module_completed": module_completed,
                           "named_children": named_child_frags,
                           })

        result.add_content(self.runtime.render_template("student_template.html", context=context))
        result.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/module.js'))
        result.initialize_js('ModuleXBlock')
        return result

    # # will get total weights and total student scores for childern blocks
    # def get_totals(self):
    #     total_weight = 0
    #     total_student_score = 0

    #     for child_id in self.children:  # pylint: disable=E1101
    #         child = self.runtime.get_block(child_id)
    #         total_weight += child.weight
    #         total_student_score += child.student_score

    #     return total_weight, total_student_score


    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ModuleXBlock",
             """<module>
                    <jsav weight="10"></jsav>
                    <jsav weight="20"></jsav>
                </module>
             """),
        ]

        # return [
        #     ("ModuleXBlock",
        #      """<vertical_demo>
        #             <module>
        #                 <jsav></jsav> 
        #             </module>
        #         </vertical_demo>
        #      """),
        # ]
