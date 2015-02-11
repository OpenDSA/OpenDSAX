/* Javascript for ModuleXBlock. */
function ModuleXBlock(runtime, element) {

    function roundPercent(number) {
        return Math.round(number * 100) / 100;
    }

    function callIfExists(obj, fn) {
        if (typeof obj[fn] == 'function') {
            return obj[fn].apply(obj, Array.prototype.slice.call(arguments, 2));
        } else {
            return undefined;
        }
    }

    function messageListener(e) {
        var score,
            complete;

        if (e.originalEvent.origin.indexOf("algoviz.org") < 0) {
            console.log("Wrong origin...");
            return;
        }

        var data = e.originalEvent.data;
        console.log("type: " + data.type + " uiid: " + data.uiid + " seed: " + data.seed);
        // console.dir(data);

        if (data.type === "jsav-exercise-grade-change" || data.type === "jsav-exercise-grade" || data.type === "jsav-exercise-step-fixed") {
            score = roundPercent(data.score.correct / data.score.total);
            complete = roundPercent((data.score.correct + data.score.undo + data.score.fix) / data.score.total);
            data.desc.score = score;
            data.desc.complete = complete;

            // Prevent event data from being transmitted on every step
            // This makes better use of the buffering mechanism and overall reduces the network traffic (removed overhead of individual requests), but it takes a while to complete and while its sending the log data isn't saved in local storage, if the user closes the page before the request completes and it fails the data will be lost
            if (complete === 1) {
                // Store the user's score when they complete the exercise
                // loop for each children and call reportProgress function on corrent child
                var children = runtime.children(element);
                for (var i = 0; i < children.length; i++) {
                    var child = children[i];
                    console.log("student completed the problem, child.seed: " + child.seed + " data.seed: " + data.seed);
                    if (child.seed === data.seed) {
                        callIfExists(child, 'reportProgress', data);
                        break;
                    }
                }
            }
        }
    }

    $(document).ready(function () {
        //remove extraneous listeners
        // $(window).off("message")
        $(window).on("message", messageListener);
        $(".total_problem_score", element).text(Math.round($(".total_problem_score", element).text()));
        $(".total_problem_weight", element).text(Math.round($(".total_problem_weight", element).text()));
    });
}