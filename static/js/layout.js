
domain = window.location.pathname.split('/')[1];
setCurrentDomain(domain);

function settingsPage() {
    window.location.href = "/" + currentDomain() + "/settings";
};

function usersPage() {
    window.location.href = "/" + currentDomain() + "/users";
};

function databasePage() {
    window.location.href = "/" + currentDomain() + "/database";
};

function messagingPage() {
    window.location.href = "/" + currentDomain() + "/messaging";
};

function profilePage() {
    window.location.href = '/user/account/';
};

function logOut() {
    localStorage.clear();

    requestHandlers = {
        200: function() {
            window.location.href = '/account/sign-in';
        }
    };
    request("POST", "/account/sign-out", null, requestHandlers)
};
