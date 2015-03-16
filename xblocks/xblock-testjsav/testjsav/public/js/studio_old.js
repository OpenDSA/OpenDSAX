function JSAVXBlockStudioEdit(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'change_problem');

    $('#jsav_problem_submit', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"problem_url": $("#jsav_problem_select", element).val()}),
            success: location.reload()
        });
    });
    $('#jsav_url_submit', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"problem_url": $("#jsav_problem_url", element).val()}),
            success: location.reload()
        });
    });

}
