function initSelect2(selector, placeholder) {
    $(document).ready(function() {
        $(selector).select2({
            placeholder: placeholder,
            allowClear: true,
        });

    });
}
