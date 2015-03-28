/* Javascript for BubblesortQuestionsXBlock. */
function BubblesortQuestionsXBlock(runtime, element) {

var handlerUrl = runtime.handlerUrl(element, 'increment_score');

    function updateCount(result) {
        
        console.dir(result);
        $('.bubblesortquestions_block', element).html(result.html);
        $('.score', element).text(result.score);
        $('button', element).click(function(eventObject) {           
            checkQuestion();
        });
    }

var question;
var a = 0;
var questions = [];
var answers = [];
var submitButton;
var nextQuestionButton;

    function checkQuestion() {

        var selected = $("#solution:checked");

        if (selected.val())
        {
                $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({"question": "correct"}),
                success: updateCount
            });
        }
        else
        {
            alert('incorrect answer');
        }
    }

    function submitAnswer() {

    }



    $(function() {
        
    $('button', element).click(function(eventObject) {
        checkQuestion();
    });


        submitButton = document.getElementById("submit");
        question = document.getElementById("question");
        nextQuestionButton = document.getElementById("nextQuestion");
        //nextQuestionButton.onclick = function(){ updateQuestion() };
        //submitButton.onclick = function(){ submitAnswer() };
    });

}
