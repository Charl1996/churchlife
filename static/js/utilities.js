
//import Calendar from 'tui-calendar'; /* ES6 */
//import "tui-calendar/dist/tui-calendar.css";
//
//// If you use the default popups, use this.
//import 'tui-date-picker/dist/tui-date-picker.css';
//import 'tui-time-picker/dist/tui-time-picker.css';

var PRIMARY_COLOR = "#2185d0";

var CALENDAR_THEME_CONFIG = {
    'week.today.color': PRIMARY_COLOR,
    'common.today.color': PRIMARY_COLOR,
    'week.today.color': PRIMARY_COLOR,
    'week.today.backgroundColor': 'rgba(81, 92, 230, 0.05)',
    'week.currentTime.color': PRIMARY_COLOR,
    'week.currentTimeLinePast.border': '1px dashed ' + PRIMARY_COLOR,
    'week.currentTimeLineBullet.backgroundColor': PRIMARY_COLOR,
    'week.currentTimeLineToday.border': '1px solid ' + PRIMARY_COLOR,
    'month.weekend.backgroundColor': '#fafafa',

};

var MONTHS = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
];

var NEW_EVENT_DATA = "new_event_data"

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

function currentDomain() {
    return localStorage.getItem('domain');
}

function setCurrentDomain(domain) {
    localStorage.setItem('domain', domain);
}

function currentUserEmail() {
    return localStorage.getItem('user_email');
}

function setCurrentUserEmail(domain) {
    localStorage.setItem('user_email', domain);
}

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
            showToast('error', "Request failed");
        },
        error: function(response, _, requestMessage) {
            if (response.status == 403) {
                showToast('error', response.responseJSON.detail);
            }
            else {
                showToast('error', requestMessage);
            }
        },
        statusCode: resultHandlers
    });
}


function navigateToLogin() {
    window.location.href = '/account/sign-in';
}
