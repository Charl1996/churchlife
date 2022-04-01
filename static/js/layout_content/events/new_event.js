
// Initialize dropdown
$('.ui.dropdown')
  .dropdown()
;

function recurringEvent() {
    return $('#series_checkbox').is(':checked');
}

$("#event_type_form").change(function() {
   if (recurringEvent()) {
    $("#event-interval").show();
    $("#to-date-picker").show();
    $('#to-date-picker-input').attr('required', true);
    $("#continuous-event-checkbox").show();
   }
   else {
    $("#event-interval").hide();
    $("#to-date-picker").hide();
    $('#to-date-picker-input').removeAttr('required');
    $("#continuous-event-checkbox").hide();
   }
});

$('#event-interval').change(function() {
    $('#event-interval').removeClass('error');
});

$("#unspecified-end-date-checkbox").change(function() {
    var noEndDate = $('#unspecified-end-date-checkbox').is(':checked');

    if (noEndDate) {
        $('#to-date-picker').addClass('disabled');
        $('#to-date-picker-input').removeAttr('required');
    }
    else {
        $('#to-date-picker').removeClass('disabled');
        $('#to-date-picker-input').attr('required', true);
    }
});

$("#tracker_checkbox").change(function() {
   var shouldTrack = $('#tracker_checkbox').is(':checked');

   if (shouldTrack) {
    $("#tracker-info").show();
   }
   else {
    $("#tracker-info").hide();
   }
});

$("#cancel-button").click(function(e) {
    e.preventDefault();
    var url = "/" + currentDomain() + "/events/";
    window.location.href = url;
});

$('form').on('submit', function(e) {
        e.preventDefault();
    var formData = new FormData(document.querySelector('form'));

    var isSeriesEvent = $('#series_checkbox').is(':checked');
    var eventType = 'series';
    var eventInterval = $('#event-interval').dropdown('get value');

    if (recurringEvent() && (eventInterval == null | eventInterval == '')) {
        $('#event-interval').addClass('error');
        showToast('error', "Please select event occurrence");
        return
    }

    if (!isSeriesEvent) {
        eventType = 'one-time';
        eventInterval = '';
    }

    var to_date = formData.get('event-to-date');

    var noEndDate = $('#unspecified-end-date-checkbox').is(':checked');

    if (noEndDate) {
        to_date = '';
    }

    var newEventData = {
        event: {
            name: formData.get('event-name'),
            type: eventType,
            interval: eventInterval,
            from_date: formData.get('event-from-date'),
            to_date: to_date,
            start_at: formData.get('event-start-time'),
            end_at: formData.get('event-end-time')
        }
    };

    var captureAttendance = $('#tracker_checkbox').is(':checked')

    if (captureAttendance) {
        var trackingInfo = {
            start_before: formData.get('start-tracking-before'),
            stop_after: formData.get('stop-tracking-after')
        }
        newEventData["attendance_tracker"] = trackingInfo;
    }

    submitCreate(newEventData);
});

function submitCreate(postData) {

    var resultHandlers = {
        200: function(response) {
            var url = "/" + currentDomain() + "/events";
            window.location.href = url;
        },
        422: function(response) {
            message = response.responseJSON.detail;
            showToast('error', message);
        }
    };

    var url = "/" + currentDomain() + "/events/new";
    request('POST', url, postData, resultHandlers);

}