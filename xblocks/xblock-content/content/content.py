"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from lms_mixin import LmsCompatibilityMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from django.template import Context, Template


class ContentXBlock(XBlock, LmsCompatibilityMixin, StudioEditableXBlockMixin):
    """
    OpenDSA content viewer
    """

    XBlock_type = String(
        help="The XBlock type", 
        scope=Scope.content, 
        default="content")

    seed = Integer(
        help="Random seed for this student", 
        scope=Scope.user_state, 
        default=0)

    contnet_type = String(
        help = "whether slideshow 'ss' or proficiency exercise 'pe'",
        default = "pe",
        scope = Scope.settings)
    
    long_name = String(
        help = "OpenDSA Content",
        default = "Quick Sort Proficiency Problem",
        scope = Scope.settings)

    short_name = String(
        help = "Problem short Name, html file name",
        default = "Quicksort",
        scope = Scope.settings)

    editable_fields = ('short_name', 'long_name')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ContentXBlock, shown to students
        when viewing courses.
        """
        result = Fragment()
        url = "public/html/"+self.short_name+".html"
        fragment = Fragment(self.resource_string(url))
        html_template = Template(self.resource_string("templates/student_view.html"))
        html_context = Context({"fragment": fragment}) 
        html_str = html_template.render(html_context)
        result.add_content(html_str)
        return result

    # author_view = studio_view

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ContentXBlock",
             """<vertical_demo>
                <content/>
                </vertical_demo>
             """),
        ]