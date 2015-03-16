function StudioEditableXBlockJSAV(runtime, element) {

    $(document).ready(function () {

        // move studio_view dom elements created by jsav_based_materials inside 
        // studio_view fragment created by utils 

        // Get elements to be moved
        var $source = $(".jsav_based_materials"),
            // Get the targent element to insert the source element after it
            $target = $('li[data-field-name = "problem_type"]', element);

        // insert the elements
        $source.insertAfter($target);

        // Call the default JS code since it's no longer registered via initialize_js
        StudioEditableXBlockMixin(runtime, element);
        // JSAVXBlockStudioEdit(runtime, element);



        // show and hide pe,av and ss dropdown lists and their options based on selected problem_type
        var $problemType = $('#xb-field-edit-problem_type', element),
            $short_name = $('#xb-field-edit-short_name', element),
            $problem_url = $('#xb-field-edit-problem_url', element),
            $problem_width = $('#xb-field-edit-problem_width', element),
            $problem_height = $('#xb-field-edit-problem_height', element),
            $required = $('#xb-field-edit-required', element),
            $threshold = $('#xb-field-edit-threshold', element),
            $long_name = $('#xb-field-edit-long_name', element),
            $js_resources = $('#xb-field-edit-js_resources', element),
            $showhide = $('#xb-field-edit-showhide', element),
            $display_name = $('#xb-field-edit-display_name', element),
            $weight = $('#xb-field-edit-weight', element),
            $peListContainer = $('.jsav_based_materials .jsav_pe', element),
            $avListContainer = $('.jsav_based_materials .jsav_av', element),
            $ssListContainer = $('.jsav_based_materials .jsav_ss', element),
            params = {
                $JXOP_fixmode: $('#xb-field-edit-JXOP_fixmode', element),
                $JXOP_code: $('#xb-field-edit-JXOP_code', element),
                $JXOP_feedback: $('#xb-field-edit-JXOP_feedback', element),
                $JOP_lang: $('#xb-field-edit-JOP_lang', element),
            };

        // hide auto filled, unchangable fields
        $short_name.closest('li').hide();
        $problem_url.closest('li').hide();
        $problem_width.closest('li').hide();
        $problem_height.closest('li').hide();
        $js_resources.closest('li').hide();
        params["$JXOP_fixmode"].closest('li').hide();
        params["$JXOP_code"].closest('li').hide();
        params["$JXOP_feedback"].closest('li').hide();
        params["$JOP_lang"].closest('li').hide();


        function getExerciseName(cssClass) {
            return $("." + cssClass + " li select :selected", element).data('name');
        }

        // shows the parameters only for the chosen exercise
        function showParameters(cssClass) {
            // hide all parameter divs
            $("." + cssClass + " #jsav_parameters div li", element).hide();
            // get the name for the selected exercise
            var selected = getExerciseName(cssClass);
            // show the parameters for the selected exercise
            $('.' + cssClass + ' #jsav_parameters div[data-name="' + selected + '"] li', element).show();
        }

        showParameters("jsav_pe");
        showParameters("jsav_av");
        showParameters("jsav_ss");

        // Change listener for exercise select drop down
        $(".jsav_material", element).change(function () {
            var parentClass = $(this).data('parentclass');
            showParameters(parentClass);
            // assign data values to jsav parameters when pe, av or ss dropdown list is changed
            assignJSAVParams($(this));
        });

        function showProblemType(problemType) {
            $peListContainer.hide();
            $avListContainer.hide();
            $ssListContainer.hide();
            if (problemType === 'pe') {
                $peListContainer.show();
            } else if (problemType === 'av') {
                $avListContainer.show();
            } else if (problemType === 'ss') {
                $ssListContainer.show();
            }
        }

        function assignJSAVParams($jsavMaterialSelectClass) {
            var $option = $('option:selected', $jsavMaterialSelectClass);
            $short_name.val($option.data('name'));
            $short_name.closest('li').addClass('is-set');
            $problem_url.val($option.data('problem-url'));
            $problem_url.closest('li').addClass('is-set');
            $problem_width.val($option.data('problem-width'));
            $problem_width.closest('li').addClass('is-set');
            $problem_height.val($option.data('problem-height'));
            $problem_height.closest('li').addClass('is-set');
            $required.val($option.data('required'));
            $required.closest('li').addClass('is-set');
            $threshold.val($option.data('threshold'));
            $threshold.closest('li').addClass('is-set');
            $long_name.val($option.data('long-name'));
            $long_name.closest('li').addClass('is-set');
            $js_resources.val($option.data('js-resources'));
            $js_resources.closest('li').addClass('is-set');
            $showhide.val($option.data('showhide'));
            $showhide.closest('li').addClass('is-set');
            $display_name.val($option.data('long-name'));
            $display_name.closest('li').addClass('is-set');
            $weight.val($option.data('weight'));
            $weight.closest('li').addClass('is-set');
        }

        // return select element 
        function getJSAVMaterialSelectClass(problemType) {
            return $('.jsav_based_materials .jsav_' + problemType + ' select.jsav_material', element);
        }

        function getJSAVOptionalParamName(problemType) {
            // console.log(problemType);
            $('.jsav_based_materials .jsav_' + problemType + ' #jsav_parameters div:first li', element).each(
                function () {
                    // console.log($(this).data('field-name') + ' ' + $('select', $(this)).val());
                    var paramName = $(this).data('field-name'),
                        paramVal = $('select', $(this)).val();
                    params['$' + paramName].val(paramVal);
                    params['$' + paramName].closest('li').addClass('is-set');
                }
            )
        }

        // get the selected problem_type    
        var problemTypeChoice = $problemType.val();
        showProblemType(problemTypeChoice);
        assignJSAVParams(getJSAVMaterialSelectClass(problemTypeChoice));
        getJSAVOptionalParamName(problemTypeChoice);


        $problemType.change(function (e) {
            var $jsavMaterialSelectClass = getJSAVMaterialSelectClass($problemType.val());
            showProblemType($problemType.val());
            assignJSAVParams($jsavMaterialSelectClass);
        });


        // Change handler to assign JOP and JXOP optional params
        $(".optionparams", element).on("change", params, function (params) {
            var paramName = $(this).closest('li').data("field-name");
            // console.log($(this).val() + ' ' + paramName);
            // console.dir(params.data);
            params.data['$' + paramName].val($(this).val());
            params.data['$' + paramName].closest('li').addClass('is-set');
        });

        // assign data values to jsav parameters when pe, av or ss dropdown list is changed
        // $(".jsav_material", element).change(function (e) {
        //     assignJSAVParams($(this));
        // });

        // $problemType.change(function (e) {
        //     showProblemType($problemType.val());
        // });


        // $field.bind("change input paste", fieldChanged);
        // $resetButton.click(function () {
        //     $field.val($wrapper.attr('data-default')); // Use attr instead of data to force treating the default value as a string
        //     $wrapper.removeClass('is-set');
        //     $resetButton.removeClass('active').addClass('inactive');
        // });
    });
}