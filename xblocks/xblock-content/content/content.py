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

    next_link = String(
        help="link to the next module", 
        scope=Scope.settings, 
        default="next_link")

    prev_link = String(
        help="link to the previous module", 
        scope=Scope.settings, 
        default="prev_link")

    next_name = String(
        help="name of the next module", 
        scope=Scope.settings, 
        default="next_name")

    prev_name = String(
        help="name of the previous module", 
        scope=Scope.settings, 
        default="prev_name")

    toc_link = String(
        help="link to the table of content", 
        scope=Scope.settings, 
        default="toc_link")

    source_link = String(
        help="link to the source rst file", 
        scope=Scope.settings, 
        default="source_link")

    seed = Integer(
        help="Random seed", 
        scope=Scope.user_state, 
        default=0)

    contnet_type = String(
        help = "whether OpenDSA contnet , header, footer or navigation bar",
        default = "content",
        values = ({"value":"content","display_name":"OpenDSA Content"}, 
                  {"value":"header","display_name":"OpenDSA Header"},
                  {"value":"footer","display_name":"OpenDSA Footer"},
                  {"value":"topnav","display_name":"OpenDSA Navigation Bar"}),
        scope = Scope.settings)
    
    long_name = String(
        help = "OpenDSA Content",
        default = "OpenDSA Content",
        scope = Scope.settings)

    short_name = String(
        help = "OpenDSA contnet name, html file name",
        default = "Quicksort",
        scope = Scope.settings)

    editable_fields = ('contnet_type', 'short_name', 'long_name','next_link','next_name',
                       'prev_link','prev_name','toc_link','source_link')

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
        if self.contnet_type == "content":
            result = Fragment()
            url = "public/html/"+self.short_name+".html"
            fragment = Fragment(self.resource_string(url))
            html_template = Template(self.resource_string("templates/student_view.html"))
            html_context = Context({"fragment": fragment}) 
            html_str = html_template.render(html_context)
            result.add_content(html_str)
            return result
        elif self.contnet_type == "topnav":
            html_context = Context({"source_link": self.source_link, 
                                    "prev_link": self.prev_link, 
                                    "prev_name": self.prev_name, 
                                    "toc_link": self.toc_link, 
                                    "next_link": self.next_link, 
                                    "next_name": self.next_name, 
                                    })
            html_template = Template(self.resource_string("templates/student_view_topnav.html"))
            fragment = Fragment(html_template.render(html_context))
            return fragment
        elif self.contnet_type == "header":
            return
        elif self.contnet_type == "footer":
            return


    def studio_view(self, context):
        fragment = super(ContentXBlock, self).studio_view(context)
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/src/studio_edit_content.js'))
        fragment.initialize_js('StudioEditableXBlockContent')
        return fragment

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