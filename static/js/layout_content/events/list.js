$(document).ready(function() {
    $('.ui.menu').menu();
});

function removeActive() {
    $('#upcoming-events-content-item').removeClass('active');
    $('#upcoming-events-content').hide();

    $('#past-events-content-item').removeClass('active');
    $('#past-events-content').hide();

    $('#all-events-content-item').removeClass('active');
    $('#all-events-content').hide();
}

function setActive(id) {
    removeActive();

    $('#' + id).show();
    $("#" + id + "-item").addClass("active");
}

function selectUpcomingEventsMenuItem() {
    setActive('upcoming-events-content');
}

function selectPastEventsMenuItem() {
    setActive('past-events-content');
}

function selectAllEventsMenuItem() {
    setActive('all-events-content');
}


function addNewEvent() {
//    Redirect to new event page
    var url = "/" + currentDomain() + "/events/new";
    window.location.href = url;
}


function deleteEvent(eventId) {
    var url = "/" + currentDomain() + "/events/" + eventId;

    resultHandlers = {
        200: function(response) {
            window.location.reload();
        },
    }

    request("DELETE", url, null, resultHandlers);
}

function cancelSessionEvent(sessionEventId) {
    var url = "/" + currentDomain() + "/events/sessions/" + sessionEventId + "/cancel";

    resultHandlers = {
        200: function(response) {
            window.location.reload();
        },
    }

    request("POST", url, null, resultHandlers);
}

function viewEvent(event_id, sessionEventId) {

}

function viewSessionEvent(sessionEventId) {
    var url = "/" + currentDomain() + "/events/sessions/" + sessionEventId;
    window.location.href = url;
}
