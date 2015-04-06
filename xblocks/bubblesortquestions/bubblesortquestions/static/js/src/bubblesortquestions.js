/* Javascript for BubblesortQuestionsXBlock. */
function BubblesortQuestionsXBlock(runtime, element) {

//Change this to whatever you need for the exercise
var maxScore = 5;


var handlerUrl = runtime.handlerUrl(element, 'getNewQuestion');
var flag = "false";
    function updateQuestion(result) {
        $('.bubblesortquestions_block', element).html(result.html);
        $('#maxScore').text(maxScore);
        flag = "false";
        $('.score', element).text(result.score);
        $('button', element).click(function(eventObject) {           
            checkQuestion();
        });
    }

    //Checks to see if the question was answered correctly. Will fetch a new question upon correct answer
    function checkQuestion() {

        var selected = $("#solution:checked");

        //Was answer right?
        if (selected.val())
        {
            //TODO: Have two button-process for correct answer choice
                $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({"question": "correct", "flag": flag}),
                success: updateQuestion
            });
        }
        else
        {
            flag = "true";
            //TODO: style for the shaking button
            alert('incorrect answer');
        }
    }

    function submitAnswer() {

    }

    //Gets executed once upon first question load
    $(function() {
        $('#maxScore').text(maxScore);
        $('button', element).click(function(eventObject) {
            checkQuestion();
        });
    });

}
