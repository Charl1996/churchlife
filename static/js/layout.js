
domain = window.location.pathname.split('/')[1];
setCurrentDomain(domain);

function summaryPage() {
    var url = "/" + currentDomain() + "/summary";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)
};


function eventsPage() {
    var url = "/" + currentDomain() + "/events";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)
};


function trackingPage() {
    var url = "/" + currentDomain() + "/tracking";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)
};


function settingsPage() {
    var url = "/" + currentDomain() + "/settings";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)
};

function usersPage() {
    var url = "/" + currentDomain() + "/users";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)
};

function databasePage() {
    var url = "/" + currentDomain() + "/database";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)

};

function messagingPage() {
    var url = "/" + currentDomain() + "/messaging";

    var requestHandlers = {
        200: function(data) {
            $("#content").html(data);
        }
    };

    request("GET", url, null, requestHandlers)
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
