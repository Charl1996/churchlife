
$('#account_create_form').submit(function(e){
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'))

    var password = formData.get('password');
    var confirmPassword = formData.get('confirm-password');

    if (password != confirmPassword) {
        show_toast('error', "Passwords don't match");
        $("#password-confirm").val('');
        $("#password").val('');
    }
    else {
        var postData = {
            'user': {
                'first_name': formData.get('first-name'),
                'last_name': formData.get('last-name'),
                'email': formData.get('email'),
                'password': password
            },
            'organisation': {
                'name': formData.get('organisation'),
                'domain': formData.get('domain'),
                'logo': formData.get('logo'),  // This needs to be figured out
            }
        }

        $.ajax({
            url: '/account/create',
            type: "POST",
            data: JSON.stringify(postData),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            fail: function() {
                show_toast('error', "Something went wrong");
            },
            statusCode: {
                200: function(response) {
                    window.location.href = '/account/sign-in?create_success=1';
                },
                422: function(response) {
                    message = response.responseJSON.detail;
                    show_toast('error', message);
                }
            }
        });
    }
    return false;
});

$('#sign_in_button').click(function () {
    window.location.href = '/account/sign-in';
});

function readURL(input) {
  if (input.files && input.files[0]) {
    $('#logo_image').show();
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#logo_image').attr('src', e.target.result).width(150).height(150);
    };

    reader.readAsDataURL(input.files[0]);
  }
}
