function JSAVXBlock(runtime, element) {
    function roundPercent(number) {
        return Math.round(number * 100) / 100;
    }

    function messageListener(e) {
        var score,
            complete;

        if (e.originalEvent.origin.indexOf("algoviz.org") < 0) {
            console.log("Wrong origin...");
            return;
        }
        var data = e.originalEvent.data;

        if (data.type === "jsav-exercise-grade-change" || data.type === "jsav-exercise-grade" || data.type === "jsav-exercise-step-fixed") {
            // On grade change events, log the user's score and submit it
            score = roundPercent(data.score.correct / data.score.total);
            // TODO: Verify with Ville how to properly calculate this
            complete = roundPercent((data.score.correct + data.score.undo + data.score.fix) / data.score.total);
            data.desc.score = score;
            data.desc.complete = complete;

            // Prevent event data from being transmitted on every step
            // This makes better use of the buffering mechanism and overall reduces the network traffic (removed overhead of individual requests), but it takes a while to complete and while its sending the log data isn't saved in local storage, if the user closes the page before the request completes and it fails the data will be lost
            if (complete === 1) {
                // Store the user's score when they complete the exercise
                reportProgress(data.score, data, data.seed);
            }
        }
    }

    $(document).ready(function() {
        //remove extraneous listeners
        $(window).off("message")
        $(window).on("message", messageListener)
        $(".problem_score", element).text(Math.round($(".problem_score", element).text()));
        $(".problem_weight", element).text(Math.round($(".problem_weight", element).text()));
    });

    function reportProgress(score, log, seed) {
        var handlerUrl = runtime.handlerUrl(element, 'report_progress');
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({
                "score": score,
                "log": log,
                "seed": seed,
                "datetime": new Date()
            }),
            success: updateProgress
        });
    }

    function updateProgress(result) {
        $(".problem_score", element).text(Math.round(result.student_score));
        $(".student_attempts", element).text(result.student_attempts);
        if (result.student_proficiency) {
            $(".problem_score", element).parent().append('<span class="problem_complete">WELL DONE</span>');
        }
    }
}