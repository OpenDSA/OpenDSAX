"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment


class BubblesortQuestionsXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    score = Integer(help="Score for the exercise", default = 0, scope=Scope.user_state)

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the BubblesortQuestionsXBlock, shown to students
        when viewing courses.
        """

        """
        Here we need to get a random file from the pool of html strings.
        We can declare an array of html strings, and get an index and random.
        Should we inject the header/score html code prior to the random question?
        """
        questionString = "static/html/bubblesort_Question2.html"



        html = self.resource_string(questionString)
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/bubblesortquestions.css"))
        frag.add_javascript(self.resource_string("static/js/src/bubblesortquestions.js"))
        frag.initialize_js('BubblesortQuestionsXBlock')
        return frag

    problem_view = student_view


    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_score(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['question'] == 'change'
        newHTML = self.resource_string("static/html/bubblesort_Question1.html")
        return {"score": newHTML}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("BubblesortQuestionsXBlock",
             """<vertical_demo>
                <bubblesortquestions/>
                </vertical_demo>
             """),
        ]
