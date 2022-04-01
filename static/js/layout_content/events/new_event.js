
// Initialize dropdown
$('.ui.dropdown')
  .dropdown()
;

$("#event_type_form").change(function() {
   var isSeriesEvent = $('#series_checkbox').is(':checked');

   if (isSeriesEvent) {
    $("#event-interval").show();
    $("#to-date-picker").show();
    $("#continuous-event-checkbox").show();
   }
   else {
    $("#event-interval").hide();
    $("#to-date-picker").hide();
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

$('form').on('submit', function(e) {
        e.preventDefault();
    var formData = new FormData(document.querySelector('form'));

    var isSeriesEvent = $('#series_checkbox').is(':checked');
    var eventType = 'series';
    var eventInterval = $('#event-interval').dropdown('get value');

    if (eventInterval == null | eventInterval == '') {
        $('#event-interval').addClass('error');
        showToast('error', "Please select event occurrence");
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
    // handle attendance
    // make post to create
});