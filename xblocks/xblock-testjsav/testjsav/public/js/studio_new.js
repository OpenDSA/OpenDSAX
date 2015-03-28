function JSAVXBlockStudioEdit(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'change_problem');


    $(document).ready(function(){
        $("#jsav_parameters div").hide();
        var selected = $("#jsav_problem_select :selected").attr('data-name')
        $('#jsav_parameters div[data-name="'+selected+'"]').show();        



    $("#jsav_problem_select").on('change', function() {
        $("#jsav_parameters div").hide();
        console.log($(this + ":selected"));
        var selected = $(this + ":selected").attr('data-name')
        
        $('#jsav_parameters div[data-name="'+selected+'"]').show();
        console.log(selected);
    });

    $('#jsav_problem_submit', element).click(function(eventObject) {
        var problem_url = $("#jsav_problem_select", element).val();
        var params = ''
        var selected = $(this + ":selected").attr('data-name')
        $('#jsav_parameters div[data-name="'+selected+'"] select').each(function() {
            if($(this).val().length>0) {
                if(params.length > 0) {
                    params += '&'+$(this).attr('id')+'='+$(this).val();
                } else {
                    params += '?'+$(this).attr('id')+'='+$(this).val();
                }
            }           
        });
        problem_url += params
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"problem_url": problem_url}),
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

    });

}

