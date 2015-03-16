function createjsav() {
    var arraySize = 8,
        initialArray = [],
        jsavArray,
        av = new JSAV("jsavcontainer");

    av.recorded(); // we are not recording an AV with an algorithm

    function initialize() {
      if (jsavArray) {
        jsavArray.clear();
        swapIndex.clear();
      }
      av.umsg("Directions: Click on all array elements from left to right to highlight them. Then click on the first and last elements to swap them."); 
      initialArray = JSAV.utils.rand.numKeys(10, 100, arraySize);

      jsavArray = av.ds.array(initialArray, {indexed: true});
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
      modelArray.swap(0, arraySize - 1);
      modeljsav.umsg("Now swap");
      modeljsav.gradeableStep();
      return modelArray;
    }
    
    // define a variable to hold the value of index to be swapped
    var swapIndex;
    
    var exercise = av.exercise(modelSolution, initialize,
                              { feedback: "continuous", compare: {class: "jsavhighlight"}});
    exercise.reset();

    function arrayClickHandler(index) {
      // if last index is highlighted, we are in "swap mode"
      if (this.isHighlight(arraySize - 1)) {
        // when in swap mode, first click on index will store that index
        // and change the font size on the value
        if (swapIndex.value() == -1) {
          swapIndex.value(index);
          // apply the CSS property change to index
          this.css(index, {"font-size": "130%"});
          av.step(); // add a step to the animation
        } else {
          // the second click (swapIndex has some value) will cause
          // the swap of indices index and stored swapIndex
          this.swap(index, swapIndex.value());
          // change the font-size back to normal
          this.css([swapIndex.value(), index], {"font-size": "100%"});
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
    };


  return exercise;
}
