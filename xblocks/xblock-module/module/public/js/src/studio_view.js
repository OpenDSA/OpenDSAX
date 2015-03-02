function ModuleXBlockStudio(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'change_problem');

    $(document).ready(function () {
        $('#moduleSubmit', element).click(function () {
            var moduleShortName = $("#moduleShortName", element).val();
            var moduleLongName = $("#moduleLongName", element).val();

            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({
                    "moduleShortName": moduleShortName,
                    "moduleLongName": moduleLongName
                }),
                success: location.reload()
            });
        });
    });
}