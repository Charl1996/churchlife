
$('.ui.dropdown')
  .dropdown()
;

var $calEl = $('#calendar').tuiCalendar({
  defaultView: 'month',
  taskView: true,
  scheduleView: true,
  useDetailPopup: true,
  template: {
    month: {
        daynames: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        startDayOfWeek: 0,
        narrowWeekend: true
    },
  }
});

// You can get calendar instance
var calendarInstance = $calEl.data('tuiCalendar');

calendarInstance.on('beforeCreateSchedule', function(event) {
   addNewEvent();
});

function goToToday() {
    calendarInstance.today();
    setCalendarMonthHeading();
}

function calendarNext() {
    calendarInstance.next();
    setCalendarMonthHeading();
}

function calendarPrev() {
    calendarInstance.prev();
    setCalendarMonthHeading();
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

function updateCalendarHeading(newHeading) {
    $("#calendar-heading").text(newHeading);
}

$("#calendar-view").change(function() {
    var calendarView = $('#calendar-view').dropdown('get value');
    calendarInstance.changeView(calendarView, true);
});

$("#custom-date-picker-input").change(function() {
    var formData = new FormData(document.querySelector('form'));
    var custom_date = formData.get('custom_date');
    calendarInstance.setDate(new Date(custom_date));

    setCalendarMonthHeading();
});

function setCalendarMonthHeading() {
    var headingText = MONTHS[calendarInstance.getDate().getMonth()] + " " + calendarInstance.getDate().getFullYear();
    updateCalendarHeading(headingText);
}

setCalendarMonthHeading();