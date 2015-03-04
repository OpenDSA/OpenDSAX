function JSAVXBlock_{{seed}}(runtime, element) {
    // _{{seed}}
    var seed = "{{seed}}",
        shortName = "{{shortName}}",
        longName = "{{longName}}",
        points = "{{points}}",
        required = "{{required}}",
        threshold = "{{threshold}}",
        problemType = "{{problemType}}",
        correctImg = "";

    // console.log("JSAVXBlock_");


    $(document).ready(function() {

        // $(element).on("jsav-log-event", function (e, data) {
        //     console.dir(data);
        //     data.seed = seed;
        //     $("body").trigger("jsav-log-event", [data]);
        // });
        if (window.ODSA[shortName] && typeof window.ODSA[shortName] === 'function') {
            window.ODSA[shortName]();
        }
        $(".problem_score", element).text(Math.round($(".problem_score", element).text()));
        $(".problem_weight", element).text(Math.round($(".problem_weight", element).text()));
    });

    function reportProgress(data) {
        var score = data.score,
            log = data,
            seed = data.seed;

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
            correctImg = result.correct_icon;
            // "/resource/jsav/public/images/correct-icon.png";
            $(".problem_complete img", element).attr('src', correctImg);
        }

        updateModuleProgress(result);

    }

    function updateModuleProgress(result) {
        var total_problem_score,
            total_problem_weight;

        $module = $("div[data-block-type='module']");
        if ($module && !result.already_proficient) {
            total_problem_score = parseInt($(".total_problem_score", $module).text()) + result.student_score;
            $(".total_problem_score", $module).text(Math.round(total_problem_score));

            // module proficiency indicator 
            // TODO: module proficiency should be calculated based on only required problems.
            total_problem_score = parseInt($(".total_problem_score", $module).text());
            total_problem_weight = parseInt($(".total_problem_weight", $module).text());
            // console.log("total_problem_score: " + total_problem_score + "total_problem_weight: " + total_problem_weight);

            if (total_problem_score == total_problem_weight) {
                correctImg = result.correct_icon;
                $(".module_complete img", $module).attr('src', correctImg);
            }
        }
    }
    return {
        "seed": seed,
        "shortName": shortName,
        "longName": longName,
        "points": points,
        "required": required,
        "threshold": threshold,
        "problemType": problemType,
        "reportProgress": reportProgress
    }
}