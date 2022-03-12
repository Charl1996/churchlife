
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
        })
        .done(function(response) {
            if (response.status_code != 200) {
                message = 'Something went wrong!';

                if (response.detail) {
                    message = response.detail;
                }

                show_toast('error', response.detail);
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
