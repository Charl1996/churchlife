
function eventsPage() {

}

function notificationsPage() {

}

function settingsPage() {

}

function profilePage() {

}

function logOut() {
    requestHandlers = {
        200: function() {
            window.location.href = '/account/sign-in';
        }
    };
    request("POST", "/account/sign-out", null, requestHandlers)
}
