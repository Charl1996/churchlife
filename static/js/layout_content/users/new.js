
function cancel() {
    var url = "/" + currentDomain() + "/users/";
    window.location.href = url;
}


$("#new_user_form").submit(function(e) {
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'));

    var password = formData.get('user-password');
    var confirmPassword = formData.get('user-password-confirm');

    if (password != confirmPassword) {
        showToast('error', "Passwords don't match");
        $("#user-password").val('');
        $("#user-password-confirm").val('');
    }
    else {
        var postData = {
            'user': {
                'first_name': formData.get('user-first-name'),
                'last_name': formData.get('user-last-name'),
                'email': formData.get('user-email'),
                'password': password
            }
        }

        var resultHandlers = {
            200: function(response) {
                var url = "/" + currentDomain() + "/users/";
                window.location.href = url;
            },
            422: function(response) {
                message = response.responseJSON.detail;
                showToast('error', message);
            }
        };

        request('POST', '/' + currentDomain() + '/users/new/', postData, resultHandlers);
        return false;
    }
});
