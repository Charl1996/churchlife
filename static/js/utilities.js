
function setCookie(name, value) {
    var validityDuration = 60*60*24;
    var expires = (new Date(Date.now()+ validityDuration*1000)).toUTCString();
    document.cookie = name + "=" + (value || "") + "; expires=" + expires + ";path=/;"
};

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
};


function request(method, url, data = null, resultHandlers = {}, headers = null) {
    if (data != null) {
        data = JSON.stringify(data);
    }

    $.ajax({
        url: url,
        type: method,
        data: data,
        contentType: 'application/json; charset=utf-8',
        headers: headers,
        fail: function() {
            show_toast('error', "Something went wrong");
        },
        error: function() {
            show_toast('error', "Something went wrong");
        },
        statusCode: resultHandlers
    });
}
