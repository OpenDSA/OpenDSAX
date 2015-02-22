"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class ContentXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
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
        help = "Problem Long Name",
        default = "Quick Sort Proficiency Problem",
        scope = Scope.settings)

    short_name = String(
        help = "Problem short Name",
        default = "Quicksort",
        scope = Scope.settings)

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
        url = "public/html/"+self.short_name+".html"
        frag = Fragment(self.resource_string(url))
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

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
