
function show_toast(toast_type, message) {
    var toast_id;

    console.log(toast_type);

    if (toast_type == 'success') {
        toast_id = '#success_toast';
    }
    if (toast_type == 'error') {
        toast_id = '#error_toast';
    }
    if (toast_type == 'warning') {
        toast_id = '#warning_toast';
    }
    $(toast_id).text(message);
    $(toast_id).show();

    setTimeout(function() {
        $(toast_id).fadeOut('fast');
    }, 5000);
}

