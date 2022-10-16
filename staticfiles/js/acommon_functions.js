function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function logoutUser() {
    let text;
    if (confirm("Are You want to logout the QAAMUUS-SYSTEM!") == true) {
       
        location.href='/logout/'
    }
}
function timeSince(date) {
    var seconds = Math.floor((new Date() - date) / 1000);

    var interval = seconds / 31536000;

    if (interval > 1) {
        return Math.floor(interval) + " years";
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + " months";
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + " days";
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + " hours";
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + " minutes";
    }
        return Math.floor(seconds) + " seconds";
    }

async function waafiPaiding(number,money) {
    var isPaided=false;
    await $.ajax({
        method: "POST",
        data: JSON.stringify({
            "schemaVersion": "1.0",
            "requestId": "10111331033",
            "timestamp": "client_timestamp",
            "channelName": "WEB",
            "serviceName": "API_PURCHASE",
            "serviceParams": {
                "merchantUid": "M0910332",
                "apiUserId": "1000527",
                "apiKey": "API-1620730280AHX",
                "paymentMethod": "mwallet_account",
                "payerInfo": { "accountNo": '252'+number },
                "transactionInfo": {
                    "referenceId": "12334",
                    "invoiceId": "7896504",
                    "amount": money.toString(),
                    "currency": "USD",
                    "description": "Test USD"
                }
            }
        }),
        headers: { 'Content-type': 'application/json;charset=ISO-8859-1' },
        url: 'https://api.waafipay.net/asm',
        success:async function (responseResp) {
            if(responseResp.responseCode=='2001'){
                isPaided=true;
            }else{
                isPaided=false;
            }
            
        },
    })
    return isPaided;
}

function getTimeCountDown(theDateTime) {
    var endDate =theDateTime;
    /* ***** Do not change this code below. ***** */
    var deadline = new Date(endDate).getTime();

    var x = setInterval(function () {
        var now = new Date().getTime();
        var t = deadline - now;
        var days = Math.floor(t / (1000 * 60 * 60 * 24));
        var hours = Math.floor((t % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((t % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((t % (1000 * 60)) / 1000);
        document.getElementById("day").innerHTML = days;
        document.getElementById("hour").innerHTML = hours;
        document.getElementById("minute").innerHTML = minutes;
        document.getElementById("second").innerHTML = seconds;

        /* Output the End date. (Only for Demo) */

        if (t < 0) {
            clearInterval(x);
            document.getElementById("demo").innerHTML = "COUNTDOWN FINISHED";
            document.getElementById("day").innerHTML = "0";
            document.getElementById("hour").innerHTML = "0";
            document.getElementById("minute").innerHTML = "0";
            document.getElementById("second").innerHTML = "0";
        }
    }, 1000);
}
