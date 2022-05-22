
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
    domElement.id = 'member-' + newElementIndex;
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
