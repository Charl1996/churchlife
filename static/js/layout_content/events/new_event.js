
$("#event_type_form").change(function() {
   var isSeriesEvent = $('#series_checkbox').is(':checked');

   if (isSeriesEvent) {
    $("#event-interval").show();
   }
   else {
    $("#event-interval").hide();
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

$("#cancel-button").click(function() {
    var url = "/" + currentDomain() + "/events/";
    window.location.href = url;
});

$("#create_event_button").click(function() {
    var formData = new FormData(document.querySelector('form'))
});
