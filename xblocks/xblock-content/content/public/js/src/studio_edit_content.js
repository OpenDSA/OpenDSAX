function StudioEditableXBlockContent(runtime, element) {

    $(document).ready(function () {

        // Call the default JS code since it's no longer registered via initialize_js
        StudioEditableXBlockMixin(runtime, element);
    });
}