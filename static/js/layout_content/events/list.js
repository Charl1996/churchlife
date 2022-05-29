
$('.ui.dropdown')
  .dropdown()
;

var $calEl = $('#calendar').tuiCalendar({
  defaultView: 'month',
  theme: CALENDAR_THEME_CONFIG,
  taskView: false,
  scheduleView: true,
  useDetailPopup: true,
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
    var eventDate;
    var calendarId;

    if (event['from_date']) {
        eventDate = event.from_date.split(" ")[0];
        calendarId = event.id;
    }
    else {
        eventDate = event.date.split(" ")[0];
        calendarId = event.event_id;
    }

    var start = new Date(eventDate + " " + event.start_time);
    var end = new Date(eventDate + " " + event.end_time);

    return {
        id: '1',
        category: 'time',
        dueDateClass: '',
        calendarId: calendarId,
        title: event.name,
        start: start,
        end: end,
    }
}

function getTimeframeSchedules(fromTime, toTime) {
    var data = {
        start: fromTime,
        end: toTime
    }
    resultHandlers = {
        200: function(response) {
            populateCalendarEvents(response);
        },
    }

    var url = "/" + currentDomain() + "/events/calendar-data";
    request("POST", url, data, resultHandlers)
}

function setCalendarEvents() {
    var calDate = calendarInstance.getDate();
    var calYear = calDate.getFullYear();
    var calMonth = calDate.getMonth();

    if (calendarInstance._viewName == "month") {
        var fromTime = new Date(calYear, calMonth-1, 1);
        var toTime = new Date(calYear, calMonth+2, 0);
    }
    else {
        if (calendarInstance._viewName == "week") {
            var fromTime = new Date(calYear, calMonth, calDate.getDate() - calDate.getDay());
            var toTime = new Date(calYear, calMonth, calDate.getDate() + (6 - calDate.getDay()));
        }
        else {
            if (calendarInstance._viewName == "day") {
                var fromTime = new Date(calYear, calMonth, calDate.getDate());
                var toTime = new Date(calYear, calMonth, calDate.getDate() + 1);
            }
        }
    }
    getTimeframeSchedules(fromTime, toTime);
}

function goToToday() {
    calendarInstance.today();
    setCalendarEvents();
    setCalendarMonthHeading();
}

function calendarNext() {
    calendarInstance.next();
    setCalendarEvents();
    setCalendarMonthHeading();
}

function calendarPrev() {
    calendarInstance.prev();
    setCalendarEvents();
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

    var refreshFromBE = false;
    if (calendarInstance._viewName == 'day') {
        refreshFromBE = true;
    }
    if (calendarInstance._viewName == 'week' && calendarView == 'month') {
        refreshFromBE = true;
    }

    calendarInstance.changeView(calendarView, true);
    if (refreshFromBE) { setCalendarEvents(); }
});

$("#custom-date-picker-input").change(function() {
    var formData = new FormData(document.querySelector('form'));
    var custom_date = formData.get('custom_date');
    calendarInstance.setDate(new Date(custom_date));

    setCalendarMonthHeading();
    setCalendarEvents();
});

function refresh() {
    setCalendarEvents();
}

function setCalendarMonthHeading() {
    var headingText = MONTHS[calendarInstance.getDate().getMonth()] + " " + calendarInstance.getDate().getFullYear();
    updateCalendarHeading(headingText);
}

setCalendarMonthHeading();
setCalendarEvents();

