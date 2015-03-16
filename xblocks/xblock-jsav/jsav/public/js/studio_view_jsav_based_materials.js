function JSAVXBlockStudioEdit(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'change_problem');

    $(document).ready(function () {

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
            var parentClass = $(this).data('parentclass'); // You need to use `val` to get the value (also, note the "()" here)
            showParameters(parentClass);
        });

        // Listener for drop down's submit button
        // $('#jsav_problem_submit', element).click(function () {
        //     var problem_url = $("#xb-field-edit-PE", element).val();
        //     var params = '';
        //     var selected = getExerciseName();
        //     $('#jsav_parameters div[data-name="' + selected + '"] select').each(function () {
        //         if ($(this).val().length > 0) {
        //             if (params.length > 0) {
        //                 params += '&' + $(this).data("name") + '=' + $(this).val();
        //             } else {
        //                 params += '?' + $(this).data("name") + '=' + $(this).val();
        //             }
        //         }
        //     });

        //     problem_url += params;

        //     $.ajax({
        //         type: "POST",
        //         url: handlerUrl,
        //         data: JSON.stringify({
        //             "problem_url": problem_url,
        //             "weight": $("#jsav_problem_weight", element).val()
        //         }),
        //         success: location.reload()
        //     });
        // });

        // $('#jsav_url_submit', element).click(function () {
        //     $.ajax({
        //         type: "POST",
        //         url: handlerUrl,
        //         data: JSON.stringify({
        //             "problem_url": $("#jsav_problem_url", element).val(),
        //             "weight": $("#jsav_problem_weight", element).val()
        //         }),
        //         success: location.reload()
        //     });
        // });
    });
}