// Initialize dropdown
$('.ui.dropdown').dropdown();

function hideDatabaseRelatedElements() {
    // Any database specific elements should be included here to hide
    $("#respondio-api-key").hide();
}

hideDatabaseRelatedElements();

$('#messaging-platform-options').change(function(instance) {
    var selectedPlatform = $('#messaging-platform-options').dropdown('get value');

    // Hide all database specific elements.
    // The selected database's elements will be made visible below.
    hideDatabaseRelatedElements();

    if (selectedPlatform == "respondio") {
        $("#respondio-api-key").show();
    }
});

function getRespondioFormData() {
    var formData = new FormData(document.querySelector('form'));

    return {
       api_key: formData.get("channel-key")
    };
}


function testConnection() {
    var selectedPlatform = $('#messaging-platform-options').dropdown('get value');
    data = {}

    if (!selectedPlatform) {
        showToast('warning', "Select a platform");
        return;
    }

    if (selectedPlatform == 'respondio') {
        data["configuration"] = getRespondioFormData();
    }

    data["platform"] = selectedPlatform;

    var resultHandlers = {
        200: function(response) {
            showToast('success', 'Connection established successfully');
        },
        403: function(response) {
            showToast('error', response.responseJSON);
        }
    };

    var url = "/" + currentDomain() + "/messaging/test-connection";
    request("POST", url, data, resultHandlers);
}

$('form').on('submit', function(e) {
    e.preventDefault();

    // Check that platform is selected
    var selectedPlatform = $('#messaging-platform-options').dropdown('get value');
    var data = {};

    if (selectedPlatform == 'respondio') {
        data["configuration"] = getRespondioFormData();
    }

    data["platform"] = selectedPlatform;

    var resultHandlers = {
        200: function(response) {
            showToast('success', 'Messaging platform successfully linked');
        },
        422: function(response) {
            message = response.responseJSON.detail;
            showToast('error', message);
        }
    };

    var url = "/" + currentDomain() + "/messaging/new";
    request("POST", url, data, resultHandlers);
});
