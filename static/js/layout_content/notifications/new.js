
// Initialize dropdown
$('.ui.dropdown')
  .dropdown()
;

function addNewNotificationMemberElement() {
    var template = $("#member-email").html();
    $("#notification-members").append(template);

    var newElementIndex = $("#notification-members").children().length-1;
    var domElement = $("#notification-members").children()[newElementIndex];
    domElement.id = 'member-' + newElementIndex;
}

function getElementEmailValue(element) {
    return element.firstElementChild.value
}

function cancel() {
    var url = "/" + currentDomain() + "/notifications/";
    window.location.href = url;
}

function validateEmail(instance) {
    var members = $("#notification-members").children();

    var duplicateError = false;

    for (let i = 0; i < members.length; i++) {
        if (members[i].id != instance.parentElement.id &&
            getElementEmailValue(members[i]) == instance.value) {
            duplicateError = true;
            break;
        }
    }

    if (duplicateError) {
        showToast('error', 'Duplicate email');
        instance.focus();
    }
}

function removeNotificationMember(instanceID) {
    var members = $("#notification-members").children();

    for (let i = 0; i < members.length; i++) {
        if (members[i].id == instanceID) {
            members[i].remove();
            break;
        }
    }
}

function get_notification_members() {
    var domMembers = $("#notification-members").children();
    var members = [];

    for (let i = 0 ; i < domMembers.length; i++) {
        var memberValue = domMembers[i].firstElementChild.value
        members.push({
            type: 'email',
            data: {
                email: memberValue
            }
        });
    }

    return members;
}

$("#new_notification_form").submit(function(e) {
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'));

    postData = {
        name: formData.get('notification-name'),
        notification_members: get_notification_members()
    }

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

    request('POST', '/' + currentDomain() + '/notifications/new/', postData, resultHandlers);
    return false;

});
