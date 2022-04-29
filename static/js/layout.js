
domain = window.location.pathname.split('/')[1];
setCurrentDomain(domain);


function eventsPage() {
    var url = "/" + currentDomain() + "/events";
    window.location.href = url;
};


function notificationsPage() {
    var url = "/" + currentDomain() + "/notifications";
    window.location.href = url;
};


function settingsPage() {
    var url = "/" + currentDomain() + "/settings";
    window.location.href = url;
};

function usersPage() {
    var url = "/" + currentDomain() + "/users";
    window.location.href = url;
};

function databasePage() {
    var url = "/" + currentDomain() + "/database";
    window.location.href = url;
};

function messagingPage() {
    var url = "/" + currentDomain() + "/messaging";
    window.location.href = url;
};

function profilePage() {
    showToast('warning', 'Not implemented yet!');
//    window.location.href = '/user/account/';
};

function logOut() {
    localStorage.clear();

    requestHandlers = {
        200: function() {
            navigateToLogin();
        }
    };
    request("POST", "/account/sign-out", null, requestHandlers)
};
