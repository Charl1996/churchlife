

function addNewNotification() {
//    Redirect to new event page
    var url = "/" + currentDomain() + "/notifications/new";
    window.location.href = url;
}

function deleteNotification(instanceID) {
    var resultHandlers = {
        200: function(response) {
            var url = "/" + currentDomain() + "/notifications/";
            window.location.href = url;
        },
        422: function(response) {
            message = response.responseJSON.detail;
            showToast('error', message);
        }
    };

    request('DELETE', '/' + currentDomain() + '/notifications/' + instanceID, null, resultHandlers);
}