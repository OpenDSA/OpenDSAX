/* Javascript for ModuleXBlock. */
function ModuleXBlock(runtime, element) {

    // console.dir(ODSA);
    var odsaUtils = ODSA.UTILS;
    var settings = ODSA.SETTINGS;
    /**
     * Keeps count of the number of events that are logged (count will be sent
     * with each event and used to determine how many, if any, events are missing)
     */
    var eventCount = 0;
    var exercises = {};
    var children = runtime.children(element);
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        if (exercises[child.shortName]) {
            continue;
        }
        exercises[child.shortName] = {
            name: child.longName,
            points: child.points,
            required: child.required,
            threshold: child.threshold,
            type: child.problemType,
            uiid: +new Date()
        };
    }

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

    function embededJSAVMsgHandler(e) {
        var score,
            complete;

        // TODO:to be configurable
        // if (e.originalEvent.origin.indexOf("opendsax.local") < 0) {
        //     console.log("Wrong origin...");
        //     return;
        // }
        var data = e.originalEvent.data;
        // console.log("type: " + data.type + " uiid: " + data.uiid + " seed: " + data.seed);
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

    // Handle data from events generated on the module page or received from embedded pages
    function JSAVEventHandler(data) {
        console.log("JSAVEventHandler");
        console.dir(data);
        var flush = false;

        // Filter out events we aren't interested in
        if (odsaUtils.discardEvents.indexOf(data.type) > -1) {
            return;
        }

        // Overwrite the av attribute with the correct value
        data.av = data.av.replace('_avc', '');

        // Initialize uiid if it doesn't exist
        if (!data.uiid && exercises[data.av]) {
            // If the event belongs to an exercise, use the exercises uiid
            // If the event belongs to the module, do nothing, page uiid will be added by odsaUtils.logEvent()
            data.uiid = exercises[data.av].uiid;
        }

        // If data.desc doesn't exist or is empty, initialize it
        if (!data.desc || data.desc === '') {
            data.desc = {};
        } else {
            // If it already exists, make sure its a JSON object
            data.desc = odsaUtils.getJSON(data.desc);
        }

        // Add the event number to the description so we can track how many events we lose
        data.desc.ev_num = eventCount++;

        var score,
            complete;

        // TODO: Make sure all additional fields of JSAV events are logged somewhere
        if (odsaUtils.ssEvents.indexOf(data.type) > -1) {
            data.desc.currentStep = data.currentStep;
            data.desc.currentStep = data.totalSteps;

            // Initializes the start time for a slideshow, the first time a user clicks on it
            if (!exercises[data.av].startTime) {
                exercises[data.av].startTime = +new Date();
            }

            // Initialize the highest step count for each slideshow so we can ensure each step is viewed
            if (!exercises[data.av].highestStep) {
                exercises[data.av].highestStep = 0;
            }

            // Increment the step count (only if the user clicked forward to a step they have not yet viewed)
            if ((data.type === 'jsav-forward' || data.type === 'jsav-backward') && data.currentStep === exercises[data.av].highestStep + 1) {
                exercises[data.av].highestStep++;
            }

            // User reached the end of a slideshow, award them credit if:
            //   - They were required to complete the slideshow and they viewed every slide (as indicated by highestStep)
            //   OR
            //   - They are not required to complete the slideshow and they simply make it to the end
            // TODO: Since this references the "settings" object its possible to open the console and set the value to 'false'
            if (data.currentStep === data.totalSteps && ((settings.REQ_FULL_SS && exercises[data.av].highestStep === data.totalSteps) || !settings.REQ_FULL_SS)) {
                data.totalTime = +new Date() - exercises[data.av].startTime;

                // TODO: Do we really want to delete this?
                // Reset the start time because the user just finished
                exercises[data.av].startTime = +new Date();

                // Prevents the exercise from being submitted multiple times if the user gets to the end and keeps clicking "Forward"
                if (!exercises[data.av].hasOwnProperty('complete')) {

                    for (var i = 0; i < children.length; i++) {
                        var child = children[i];
                        console.log("student completed the problem, child.shortName " + child.shortName + " data.av: " + data.av);
                        if (child.shortName === data.av) {
                            callIfExists(child, 'reportProgress', data);
                            break;
                        }
                    }

                    // storeExerciseScore(data.av, 1, data.totalTime);
                    // updateProfDisplay(data.av);
                    flush = true;

                    // Add the flag that prevents multiple submissions
                    exercises[data.av].complete = true;
                }
            } else {
                // Remove the flag
                delete exercises[data.av].complete;
            }
        } else if (data.type === "jsav-array-click") {
            data.desc.index = data.index;
            data.desc.arrayID = data.arrayid;
        } else if (data.type === "jsav-exercise-grade-change" || data.type === "jsav-exercise-grade" || data.type === "jsav-exercise-step-fixed") {
            // On grade change events, log the user's score and submit it
            score = odsaUtils.roundPercent(data.score.correct / data.score.total);
            // TODO: Verify with Ville how to properly calculate this
            complete = odsaUtils.roundPercent((data.score.correct + data.score.undo + data.score.fix) / data.score.total);
            data.desc.score = score;
            data.desc.complete = complete;

            // Prevent event data from being transmitted on every step
            // This makes better use of the buffering mechanism and overall reduces the network traffic (removed overhead of individual requests), but it takes a while to complete and while its sending the log data isn't saved in local storage, if the user closes the page before the request completes and it fails the data will be lost
            if (complete === 1) {
                // Store the user's score when they complete the exercise
                storeExerciseScore(data.av, score, data.totalTime, data.score.fix);
                updateProfDisplay(data.av);
                flush = true;
            }
        } else if (data.type === "odsa-award-credit") {
            // Store completion credit
            storeExerciseScore(data.av, 1, data.totalTime);
            updateProfDisplay(data.av);
            flush = true;
        }

        if (odsaUtils.scoringServerEnabled()) {
            // Save the event in localStorage
            if (!data.logged) {
                delete data.logged; // In case it explicitly says 'false'
                //odsaUtils.logEvent(data);
            }

            if (flush) {
                //flushStoredData();
            }
        }
    }

    function sendLogData(){
      //console.dir(localStorage);
      //console.log(ODSA.SETTINGS.LOGGING_SERVER);

      var handlerUrl = runtime.handlerUrl(element, 'storeLogData');

      //There is Something to Send to the server
      if(localStorage.length !== 0){

        $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify(localStorage),
                success: logDataStored,
                error: function (data){
                    console.error("Error sending data to server");
                }
              });
      }
    }

    function logDataStored(data){
      //console.log(data);
      console.log("Event data of size "+data+" are logged and successfully saved on server");
      localStorage.clear();
    } 

    $(document).ready(function () {
        //remove extraneous listeners
        // $(window).off("message")
        $(window).on("message", embededJSAVMsgHandler);
        $("body").on("jsav-log-event", function (e, data) {
            JSAVEventHandler(data);
        });
        $(".total_problem_score", element).text(Math.round($(".total_problem_score", element).text()));
        $(".total_problem_weight", element).text(Math.round($(".total_problem_weight", element).text()));

        //Timer to flush the data in localStorage to EDX server
        window.setInterval(sendLogData, 5000);
    });
}
