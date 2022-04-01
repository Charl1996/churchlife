
$("#event_type_form").change(function() {
   var isSeriesEvent = $('#series_checkbox').is(':checked');

   if (isSeriesEvent) {
    $("#event-interval").show();
    $("#continuous-event-checkbox").show();
   }
   else {
    $("#event-interval").hide();
    $("#continuous-event-checkbox").hide();
   }
});

$('.ui.dropdown')
  .dropdown()
;

$("#unspecified-end-date-checkbox").change(function() {
    var noEndDate = $('#unspecified-end-date-checkbox').is(':checked');

    if (noEndDate) {
        $('#to-date-picker').addClass('disabled');
    }
    else {
        $('#to-date-picker').removeClass('disabled');
    }
});

$("#tracker-checkbox").change(function() {
   var shouldTrack = $('#tracker-checkbox').is(':checked');

   if (shouldTrack) {
    $("#tracker-start-before").show();
   }
   else {
    $("#tracker-start-before").hide();
   }
});

$("#cancel-button").click(function(e) {
    e.preventDefault();
    var url = "/" + currentDomain() + "/events/";
    window.location.href = url;
});

$("#create_event_button").click(function(e) {
    e.preventDefault();
    var formData = new FormData(document.querySelector('form'));

    var isSeriesEvent = $('#series_checkbox').is(':checked');
    var eventType = 'series';
    var eventInterval = $('#event-interval').value;

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
    debugger;
    // handle attendance
    // make post to create
});