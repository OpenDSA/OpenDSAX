var samplePRO = {};
$(document).ready(function () {
    var arraySize = 8,
        initialArray = [],
        jsavArray,
        av = new JSAV("jsavcontainer"),
        channel,
        // state object will be created by getState fn. edX will call getState fn
        // to get the current state the applicaiton.
        // setState fn will reset this object. edX will call setState fn and pass 
        // state object to revert the application beck to it previous state saved in edx side.
        state = {};

    // Establish a channel only if this application is embedded in an iframe.
    // This will let the parent window communicate with this application using
    // RPC and bypass SOP restrictions.
    if (window.parent !== window) {
        channel = Channel.build({
            window: window.parent,
            origin: "*",
            scope: "JSInput"
        });

        channel.bind("getGrade", getGrade);
        channel.bind("getState", getState);
        channel.bind("setState", setState);
    }

    av.recorded(); // we are not recording an AV with an algorithm

    function initialize() {
        if (jsavArray) {
            jsavArray.clear();
            swapIndex.clear();
        }
        av.umsg("Directions: Click on all array elements from left to right to highlight them. Then click on the first and last elements to swap them.");

        if (state.initialArray) {
            initialArray = state.initialArray;
        } else {
            initialArray = JSAV.utils.rand.numKeys(10, 100, arraySize);
        }

        jsavArray = av.ds.array(initialArray, {
            indexed: true
        });
        swapIndex = av.variable(-1);

        // bind a function to handle all click events on the array
        jsavArray.click(arrayClickHandler);
        return jsavArray;
    }

    function modelSolution(modeljsav) {
        var modelArray = modeljsav.ds.array(initialArray);
        modeljsav.displayInit();
        for (var i = 0; i < arraySize; i++) {
            modelArray.highlight(i);
            modeljsav.umsg("Highlight " + i);
            modeljsav.gradeableStep();
        }
        // swap the first and last element
        modeljsav.umsg("Now swap");
        modelArray.swap(0, arraySize - 1);
        modeljsav.gradeableStep();
        return modelArray;
    }

    // define a variable to hold the value of index to be swapped
    var swapIndex;

    function arrayClickHandler(index) {
        // if last index is highlighted, we are in "swap mode"
        if (this.isHighlight(arraySize - 1)) {
            // when in swap mode, first click on index will store that index
            // and change the font size on the value
            if (swapIndex.value() == -1) {
                swapIndex.value(index);
                // apply the CSS property change to index
                this.css(index, {
                    "font-size": "130%"
                });
                av.step(); // add a step to the animation
            } else {
                // the second click (swapIndex has some value) will cause
                // the swap of indices index and stored swapIndex
                this.swap(index, swapIndex.value());
                // change the font-size back to normal
                this.css([swapIndex.value(), index], {
                    "font-size": "100%"
                });
                swapIndex.value(-1);
                exercise.gradeableStep(); // this step will be graded
            }
        } else { // we are in highlight mode
            // highlight the index
            this.highlight(index);
            if (index == (arraySize - 1)) {
                av.umsg("Good, now swap the first and last index");
            }
            // mark this as a gradeable step; also handles continuous feedback
            exercise.gradeableStep();
        }
    }


    var exercise = av.exercise(modelSolution, initialize, {
        feedback: "continuous",
        compare: {
            class: "jsavhighlight"
        }
    });
    exercise.reset();

    function getGrade() {
        // The following return value may or may not be used to grade
        // server-side.
        // If getState and setState are used, then the Python grader also gets
        // access to the return value of getState and can choose it instead to
        // grade.
        return JSON.stringify(exercise.score);
    }

    function getState() {
        var state = {},
            studentStates;
        studentStates = JSON.parse(exercise._jsondump());
        // return current state which is the last object returned by _jsondump fn
        state.lastState = studentStates[studentStates.length - 1];
        state.initialArray = exercise.initialStructures._values;
        state.score = exercise.score;
        return (JSON.stringify(state));
    }

    function setState() {
        // This function will be called with 1 argument when JSChannel is not used,
        // 2 otherwise. In the latter case, the first argument is a transaction
        // object that will not be used here
        // (see http://mozilla.github.io/jschannel/docs/)
        var stateStr = arguments.length === 1 ? arguments[0] : arguments[1];
        state = JSON.parse(stateStr);
        exercise.reset();

        if (state.score) {
            exercise.score.undo = state.score.undo;
            exercise.score.fix = state.score.fix;
        }

        if (state.lastState) {
            var i = 1;

            function delayLoop() {
                var index;
                setTimeout(function () {
                    index = state.lastState.ind[i - 1];
                    if (index.cls) {
                        // simulate student clicks
                        // TODO: should find a better way to do this, to be part of JSAV API?
                        $("#jsavcontainer .jsavindex:nth-child(" + i + ") .jsavvaluelabel").trigger("click");
                    } else {
                        return;
                    }
                    i += 1;
                    if (i <= state.lastState.ind.length) {
                        delayLoop();
                    }
                }, 500);
            }
            delayLoop(); //  start the loop
        }

    }
    samplePRO = {
        getState: getState,
        setState: setState,
        getGrade: getGrade
    };
}());