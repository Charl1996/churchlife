
// This code shows the "success" toast when a new account has been created
// and the user is redirected to this page again.
var urlParams = new URLSearchParams(location.search);
show_success_toast = urlParams.get('update-success');

if (show_success_toast) {
    showToast('success', 'Organisation details successfully updated');
}


$('form').on('submit', function(e) {
    e.preventDefault();

    var formData = new FormData(document.querySelector('form'));
    var data = {
        name: formData.get('organisation-name')
    }

    var resultHandlers = {
        200: function(response) {
            var url = "/" + currentDomain() + "/settings?update-success=1";
            window.location.href = url;
        },
        422: function(response) {
            message = response.responseJSON.detail;
            showToast('error', message);
        }
    };

    var url = "/" + currentDomain() + "/settings";
    request("POST", url, data, resultHandlers);
});
