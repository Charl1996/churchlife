function setCurrentStep(step) {
    localStorage.setItem('current-step', step);
}

function getCurrentStep(step) {
    return localStorage.getItem('current-step');
}

setCurrentStep('1');

$("#next_button").click(function() {
    step = getCurrentStep();

    if (step == '1') {
        $("#user-details").hide();
        $("#step-1").removeClass("active");

        $("#org-details").show();
        $("#step-2").removeClass("disabled");
        $("#step-2").addClass("active");
        $("#previous-button").removeClass("disabled");

        setCurrentStep('2');
        $("#next_button").addClass("disabled");
    }

});

function previous() {
    step = getCurrentStep();

    if (step == '2') {
        $("#user-details").show();
        $("#step-1").addClass("active");

        $("#org-details").hide();
        $("#step-2").removeClass("active");
        $("#previous-button").addClass("disabled");

        $("#next_button").removeClass("disabled");
        setCurrentStep('1');
    }
}


$('#account_create_form').submit(function(e) {
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'));

    var password = formData.get('password');
    var confirmPassword = formData.get('confirm-password');

    if (password != confirmPassword) {
        showToast('error', "Passwords don't match");
        $("#password-confirm").val('');
        $("#password").val('');
    }
    else {
        var uploadedFile = $('#logoImageInput')[0].files;
        var logo;

        if (uploadedFile.length > 0) {
            logo = uploadedFile[0];
        }

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
                'logo': logo
            }
        }

        var resultHandlers = {
            200: function(response) {
                if (logo) {
                    var fd = new FormData();
                    fd.append('file', logo);

                    //  Upload organisation logo
                    $.ajax({
                        url: '/' + formData.get('domain') + '/upload-logo',
                        type: "POST",
                        data: fd,
                        processData: false,
                        contentType: false,
                        statusCode: {
                            200: function () {
                                window.location.href = '/account/sign-in?create_success=1';
                            }
                        }
                    });
                }
                else {
                    window.location.href = '/account/sign-in?create_success=1';
                }
            },
            422: function(response) {
                message = response.responseJSON.detail;
                showToast('error', message);
            }
        };

        request('POST', '/account/create', postData, resultHandlers);

        return false;
    }
});

$('#sign_in_button').click(function () {
    navigateToLogin();
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
