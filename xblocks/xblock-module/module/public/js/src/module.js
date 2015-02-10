/* Javascript for ModuleXBlock. */
function ModuleXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function (eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({
                "hello": "world"
            }),
            success: updateCount
        });
    });

    $(function ($) {
        $(".total_problem_score", element).text(Math.round($(".total_problem_score", element).text()));
        $(".total_problem_weight", element).text(Math.round($(".total_problem_weight", element).text()));
    });
}