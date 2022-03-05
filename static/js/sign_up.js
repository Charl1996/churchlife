
$('#signup_form').submit(function(e){
    e.preventDefault();

    var postData = new FormData(document.querySelector('form'))

    $.ajax({
        url: 'http://localhost:8082/account/sign-up',
        type: "POST",
        data: postData,
        processData: false,
        contentType: false,
        success: function(res) {
            alert('Success!');
        },
        error: function(res) {
            alert('Error occurred!');
        }
    });

    return false;
});
