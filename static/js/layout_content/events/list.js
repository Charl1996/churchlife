
$('.ui.dropdown')
  .dropdown()
;

var $calEl = $('#calendar').tuiCalendar({
  defaultView: 'month',
  theme: CALENDAR_THEME_CONFIG,
  taskView: false,
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
    // Set data in localstorage for auto-population
    var data = {
        datetime: new Date(event.start)
    };

    localStorage.setItem(NEW_EVENT_DATA, JSON.stringify(data));
    addNewEvent();
});

function populateCalendarEvents(events) {
    var schedules = [];

    for (i=0; i < events.length; i++) {
        schedule = parseToCalendarSchedule(events[i]);
        schedules.push(schedule);
    }

    updateCalendarSchedules(schedules);
}

function updateCalendarSchedules(schedules) {
    calendarInstance.clear();
    calendarInstance.createSchedules(schedules);
}

function parseToCalendarSchedule(event) {
    var eventDate = event.from_date.split(" ")[0];
    var start = new Date(eventDate + " " + event.start_time);
    var end = new Date(eventDate + " " + event.end_time);

    return {
        id: '1',
        category: 'time',
        dueDateClass: '',
        calendarId: event.id,
        title: event.name,
        start: start,
        end: end,
    }
}

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

var events = $('#events-data').data("events");
populateCalendarEvents(events);
