
$('#signup_form').submit(function(e){
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'))

    var password = formData.get('password');
    var confirmPassword = formData.get('confirm-password');

    if (password != confirmPassword) {
        alert("Password don't match!");
        $("#password-confirm").val('');
        $("#password").val('');
    }
    else {
        var postData = {
            'first_name': formData.get('first-name'),
            'last_name': formData.get('last-name'),
            'email': formData.get('email'),
            'domain': formData.get('domain'),
            'password': password,
        }

        $.ajax({
            url: '/account/create',
            type: "POST",
            data: JSON.stringify(postData),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(res) {
                window.location.href = res.redirect_url;
            },
            error: function(res) {
                alert('Error occurred!');
            }
        });
    }
    return false;
});

$('#sign_in_button').click(function () {
    window.location.href = '/account/sign-in';
});
