
// This code shows the "success" toast when a new account has been created
// and the user is redirected to this page again.
var urlParams = new URLSearchParams(location.search);
created_account_successfully_redirect = urlParams.get('create_success');

if (created_account_successfully_redirect) {
    show_toast('success', 'Account created successfully');
}


function signIn(postData) {
    resultHandlers = {
        200: function(response) {
            goToOrganisationsPage();
        },
        403: function(response) {
            message = response.responseJSON.detail;
            show_toast('error', message);
        }
    }

    request("POST", "/account/sign-in", postData, resultHandlers);
};

function goToOrganisationsPage() {
    window.location.href = '/account/organisations';
};


$('#signin_form').submit(function(e){
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'))

    var postData = {
        'email': formData.get('email'),
        'password': formData.get('password'),
    }

    signIn(postData);
    return false;
});

$('#sign_up_button').click(function () {
    window.location.href = '/account/create';
});