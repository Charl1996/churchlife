// Initialize dropdown
$('.ui.dropdown').dropdown();

function hideDatabaseRelatedElements() {
    // Any database specific elements should be included here to hide
    $("#breeze-domain").hide();
    $("#breeze-api-key").hide();
}

hideDatabaseRelatedElements();

$('#database-platform-options').change(function(instance) {
    var selectedPlatform = $('#database-platform-options').dropdown('get value');

    // Hide all database specific elements.
    // The selected database's elements will be made visible below.
    hideDatabaseRelatedElements();

    if (selectedPlatform == "breeze") {
        $("#breeze-domain").show();
        $("#breeze-api-key").show();
    }
});

function getBreezeFormData() {
    var formData = new FormData(document.querySelector('form'));

    return {
       subdomain: formData.get("breeze-subdomain"),
       api_key: formData.get("api-key")
    };
}

function testConnection() {
    var selectedPlatform = $('#database-platform-options').dropdown('get value');
    data = {}

    if (!selectedPlatform) {
        showToast('warning', "Select a platform");
        return;
    }

    if (selectedPlatform == 'breeze') {
        data["configuration"] = getBreezeFormData();
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

    var url = "/" + currentDomain() + "/database/test-connection";
    request("POST", url, data, resultHandlers);
}

$('form').on('submit', function(e) {
    e.preventDefault();

    // Check that platform is selected
    var selectedPlatform = $('#database-platform-options').dropdown('get value');
    var data = {};

    if (selectedPlatform == 'breeze') {
        data["configuration"] = getBreezeFormData();
    }

    data["platform"] = selectedPlatform;

    var resultHandlers = {
        200: function(response) {
            showToast('success', 'Database successfully linked');
        },
        422: function(response) {
            message = response.responseJSON.detail;
            showToast('error', message);
        }
    };

    var url = "/" + currentDomain() + "/database/new";
    request("POST", url, data, resultHandlers);
});

function getDatabaseEntities() {
    var resultHandlers = {
        200: function(response) {
            $("#database-entities-list").html(response);
            $("#loader").hide();
        },
        422: function(response) {
            message = response.responseJSON.detail;
            showToast('error', message);
        }
    };

    var url = "/" + currentDomain() + "/database/entities";
    request("GET", url, null, resultHandlers);
}

function viewEntityDetails(entityRemoteId) {
    showToast('warning', "Not implemented yet")
}


var database = $("#database-data").data("database");

if (database) {
    getDatabaseEntities();
}
