/* Javascript for BubblesortQuestionsXBlock. */
function BubblesortQuestionsXBlock(runtime, element) {

var handlerUrl = runtime.handlerUrl(element, 'increment_score');

    function updateCount(result) {
        
        console.dir(result);
        //$('.bubblesortquestions_block', element).innerHTML = result.score;
        $('.bubblesortquestions_block', element).html(result.score);

    }

var question;
var a = 0;
var questions = [];
var answers = [];
var submitButton;
var nextQuestionButton;

    function updateQuestion() {
        submitButton.style.display = 'block';
        nextQuestionButton.style.display = 'none';
    if (a <=3)    
        {
        questions[a].style.display = 'none';
        questions[a+1].style.display = 'block';
        a++;
        }
    }

    function submitAnswer() {

        if (a == 0)
        {
            if(document.getElementById('question1_answer4').checked)
            {
                submitButton.style.display = 'none';
                nextQuestionButton.style.display = 'block';
            }
        }
        else if (a == 1)
        {
            if(document.getElementById('question2_answer1').checked)
            {
                submitButton.style.display = 'none';
                nextQuestionButton.style.display = 'block';
            }
        }
        else if (a == 2)
        {
            if(document.getElementById('question3_answer1').checked)
            {
                submitButton.style.display = 'none';
                nextQuestionButton.style.display = 'block';
            }
        }
        else if (a == 3)
        {
            if(document.getElementById('question4_answer1').checked)
            {
                submitButton.style.display = 'none';
                nextQuestionButton.style.display = 'block';
                nextQuestionButton.innerHTML = 'Correct!';
                nextQuestionButton.disabled = 'true';
            }
        }
    }

    $('button', element).click(function(eventObject) {
        
        if ('answer was correct')
        {
            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({"question": "change"}),
                success: updateCount
            });
        }
    });


    $(function() {
        questions[0] = document.getElementById("form1");
        questions[1] = document.getElementById("form2");
        questions[2] = document.getElementById("form3");
        questions[3] = document.getElementById("form4");

        submitButton = document.getElementById("submit");
        question = document.getElementById("question");
        nextQuestionButton = document.getElementById("nextQuestion");
        nextQuestionButton.onclick = function(){ updateQuestion() };
        submitButton.onclick = function(){ submitAnswer() };
    });

}
