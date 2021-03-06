
// Initialize dropdown
$('.ui.dropdown')
  .dropdown()
;

function setCurrentStep(step) {
    localStorage.setItem('current-step', step);
}

function getCurrentStep(step) {
    return localStorage.getItem('current-step');
}

setCurrentStep('1');

function addDatumElement() {
    var index = $("#data-members").children().length-1;
    var previousDomElement = $("#data-members").children()[index];
    var previousDomElementValue = previousDomElement.children[0].children[0].value;

    if (!previousDomElementValue) {
        showToast('warning', 'Please populate "Key" field first');
        previousDomElement.children[0].children[0].focus();
        return;
    }

    $("#no-data-notification").hide();

    var template = $("#add-datum").html();
    $("#data-members").append(template);

    var newElementIndex = $("#data-members").children().length-1;
    var domElement = $("#data-members").children()[newElementIndex];

    domElement.id = 'data-' + newElementIndex;

    checkboxInput = domElement.children[1].children[0].children[0];
    checkboxLabel = domElement.children[1].children[0].children[1];

    checkboxInput.id = 'bool-field-' + newElementIndex;
    checkboxLabel.setAttribute("for", checkboxInput.id);
}

function removeDatum(instanceID) {
    var members = $("#data-members").children();

    for (let i = 0; i < members.length; i++) {
        if (members[i].id == instanceID) {
            members[i].remove();
            break;
        }
    }
}

function recurringEvent() {
    return $('#series_checkbox').is(':checked');
}

function handleEventTypeUI() {
   if (recurringEvent()) {
    $("#event-interval").show();
    $("#to-date-picker").show();
    $('#to-date-picker-input').attr('required', true);
    $("#continuous-event-checkbox").show();
    // Update label values
    $("#event-start-date-label").html("First event");
    $("#event-end-date-label").html("Last event");
   }
   else {
    $("#event-interval").hide();
    $("#to-date-picker").hide();
    $('#to-date-picker-input').removeAttr('required');
    $("#continuous-event-checkbox").hide();
    // Update label values
    $("#event-start-date-label").html("Event date");
   }
}

$("#event-start-time").change(function() {
    var startTimeString = $("#event-start-time").val();
    var timeSplit = startTimeString.split(":");

    var startTime = parseInt(timeSplit[0]);
    var endTime = startTime + 1;

    if (endTime > 23) { endTime = 0 }

    var endTimeString = endTime.toString();
    if (endTimeString.length == 1) { endTimeString = "0" + endTimeString }

    $("#event-end-time").val(endTimeString + ":" + timeSplit[1]);
});

$("#event_type_form").change(function() {
    handleEventTypeUI();
});

$('#event-interval').change(function() {
    $('#event-interval').removeClass('error');
});

//$('#event-notifications').change(function() {
//    $('#event-notifications').removeClass('error');
//});

//$('#notification-trigger').change(function() {
//    $('#notification-trigger').removeClass('error');
//});

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

function cancel() {
    var url = "/" + currentDomain() + "/events/";
    window.location.href = url;
}

function addNotification() {
    var url = "/" + currentDomain() + "/notifications/new";
    window.location.href = url;
}

function extractNotificationId(stringId) {
    return stringId.split("-")[1];
}

$("#next_button").click(function() {
    step = getCurrentStep();

    if (step == '1') {
        $("#event-details").hide();
        $("#step-1").removeClass("active");

        $("#event-data").show();
        $("#step-2").removeClass("disabled");
        $("#step-2").addClass("active");
        $("#previous-button").removeClass("disabled");

        setCurrentStep('2');
    }
    if (step == '2') {
        $("#event-data").hide();
        $("#step-2").removeClass("active");

        $("#tracker-info").show();
        $("#step-3").removeClass("disabled");
        $("#step-3").addClass("active");

        setCurrentStep('3');
    }
    if (step == '3') {
        $("#tracker-info").hide();
        $("#step-3").removeClass("active");

        $("#notification-info").show();
        $("#step-4").removeClass("disabled");
        $("#step-4").addClass("active");

        $("#next_button").addClass("disabled");
        $("#create_event_button").removeClass("disabled");

        setCurrentStep('4');
    }

});

function previous() {
    step = getCurrentStep();

    if (step == '2') {
        $("#event-details").show();
        $("#step-1").addClass("active");

        $("#event-data").hide();
        $("#step-2").removeClass("active");
        $("#previous-button").addClass("disabled");

        setCurrentStep('1');
    }
    if (step == '3') {
        $("#event-data").show();
        $("#step-2").addClass("active");

        $("#tracker-info").hide();
        $("#step-3").removeClass("active");


        setCurrentStep('2');
    }
    if (step == '4') {
        $("#tracker-info").show();
        $("#step-3").addClass("active");

        $("#notification-info").hide();
        $("#step-4").removeClass("active");

        $("#next_button").removeClass("disabled");
        $("#create_event_button").addClass("disabled");
        setCurrentStep('3');
    }
}

function getCustomData() {
    debugger;
    var dataMembersElement = $("#data-members")[0]

    data = []
    for (i=0; i < dataMembersElement.children.length; i++) {
        var childElement = dataMembersElement.children[i];
        var inputElement = childElement.children[0].children[0];
        var checkboxElement = childElement.children[1].children[0].children[0];

        data.push({
            is_bool: checkboxElement.checked,
            field_name: inputElement.value
        })
    }

    return data
}

//$('form').on('submit', function(e) {
$("#create_event_button").click(function(e) {
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

//    var eventNotification = $('#event-notifications').dropdown('get value');
//    var eventNotificationTrigger = $('#notification-trigger').dropdown('get value');
//
//    if (!eventNotification) {
//        $('#event-notifications').addClass('error');
//        showToast('error', "Please select notification group");
//        return
//    }
//
//    if (!eventNotificationTrigger) {
//        $('#notification-trigger').addClass('error');
//        showToast('error', "Please select notification trigger");
//        return
//    }

    var newEventData = {
        event: {
            name: formData.get('event-name'),
            type: eventType,
            interval: eventInterval,
            from_date: formData.get('event-from-date'),
            to_date: to_date,
            start_time: formData.get('event-start-time'),
            end_time: formData.get('event-end-time'),
            event_data: getCustomData()
        }
    };

    var trackingInfo = {
        start_before: formData.get('start-tracking-before'),
        stop_after: formData.get('stop-tracking-after'),
//        triggers: [
//            {
//                type: eventNotificationTrigger,
//                notification_id: extractNotificationId(eventNotification)
//            }
//        ]
        }

    newEventData["attendance_tracking"] = trackingInfo;

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

handleEventTypeUI();

if (localStorage.getItem(NEW_EVENT_DATA)) {
    // Pre-populate datetime info
    var newEventData = JSON.parse(localStorage.getItem(NEW_EVENT_DATA))

    if (newEventData.datetime) {
        // Handle from date
        var storedDate = new Date(newEventData.datetime);

        var day = ("0" + storedDate.getDate()).slice(-2);
        var month = ("0" + (storedDate.getMonth() + 1)).slice(-2);
        var fullDate = storedDate.getFullYear()+"-"+(month)+"-"+(day) ;

        var $fromDate = $("#from-date-picker-input");
        $fromDate.val(fullDate);

        // Handle time
        var starthours = storedDate.getHours();
        var endhours = starthours + 1;
        if (endhours > 23) { endhours = 0 }

        var starthoursString = starthours.toString();
        var endhoursString = endhours.toString();

        if (starthoursString.length == 1) { starthoursString = '0' + starthoursString }
        if (endhoursString.length == 1) { endhoursString = '0' + endhoursString }

        var minutes = storedDate.getMinutes();
        var minutesString = minutes.toString();

        if (minutesString === '0') { minutesString = "00" }

        var defaultStartTime = starthoursString + ":" + minutesString;
        var defaultEndTime = endhoursString + ":" + minutesString;

        var $startTime = $("#event-start-time");
        var $endTime = $("#event-end-time");

        $startTime.val(defaultStartTime);
        $endTime.val(defaultEndTime);
    }
}
