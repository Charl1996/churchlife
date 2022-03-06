
$('#signin_form').submit(function(e){
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'))

    var postData = {
        'email': formData.get('email'),
        'password': formData.get('password'),
    }

    $.ajax({
        url: '/account/sign-in',
        type: "POST",
        data: JSON.stringify(postData),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function(res) {
            window.location.href = res.redirect_url;
        },
        error: function(res) {
            // Check for status codes
            alert('Error occurred!');
        }
    });
    return false;
});

$('#sign_up_button').click(function () {
    window.location.href = '/account/sign-up';
});