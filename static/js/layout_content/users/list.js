
function inviteNewUser() {
    var url = "/" + currentDomain() + "/users/new";
    window.location.href = url;
}


function removeClicked(instanceId) {


    var url = "/" + currentDomain() + "/users/" + instanceId;

    resultHandlers = {
        200: function() {
            window.location.reload();
        }
    }

    request("DELETE", url, null, resultHandlers);
}

function editClicked(instanceId) {
    alert(instanceId);
}
