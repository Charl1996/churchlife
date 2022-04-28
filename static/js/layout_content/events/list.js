$(document).ready(function() {
    $('.ui.menu').menu();
});

function removeActive() {
    $('#upcoming-events-content-item').removeClass('active');
    $('#upcoming-events-content').hide();

    $('#past-events-content-item').removeClass('active');
    $('#past-events-content').hide();
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


function addNewEvent() {
//    Redirect to new event page
    var url = "/" + currentDomain() + "/events/new";
    window.location.href = url;
}


function cancelEvent(event) {
    return
}


function viewEvent(event) {
    return
}