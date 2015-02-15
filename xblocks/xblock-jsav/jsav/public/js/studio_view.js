function JSAVXBlockStudioEdit(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'change_problem');

    $(document).ready(function () {

        function getExerciseName() {
                return $("#jsav_problem_select :selected", element).data("name");
            }
            // shows the parameters only for the chosen exercise
        function showParameters() {
            // hide all parameter divs
            $("#jsav_parameters div", element).hide();
            // get the name for the selected exercise
            var selected = getExerciseName();
            // show the parameters for the selected exercise
            $('#jsav_parameters div[data-name="' + selected + '"]', element).show();
        }

        showParameters();

        // Change listener for exercise select drop down
        $("#jsav_problem_select", element).change(showParameters);

        // Listener for drop down's submit button
        $('#jsav_problem_submit', element).click(function () {
            var problem_url = $("#jsav_problem_select", element).val();
            var params = '';
            var selected = getExerciseName();
            // 
            $('#jsav_parameters div[data-name="' + selected + '"] select').each(function () {
                if ($(this).val().length > 0) {
                    if (params.length > 0) {
                        params += '&' + $(this).data("name") + '=' + $(this).val();
                    } else {
                        params += '?' + $(this).data("name") + '=' + $(this).val();
                    }
                }
            });

            problem_url += params;

            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({
                    "problem_url": problem_url,
                    "weight": $("#jsav_problem_weight", element).val()
                }),
                success: location.reload()
            });
        });

        $('#jsav_url_submit', element).click(function () {

            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({
                    "problem_url": $("#jsav_problem_url", element).val(),
                    "weight": $("#jsav_problem_weight", element).val(),
                    "threshold": $("#jsav_problem_threshold", element).val(),
                    "required": $('#jsav_problem_required').is(":checked"),
                }),
                success: location.reload()
            });
        });

    });
}