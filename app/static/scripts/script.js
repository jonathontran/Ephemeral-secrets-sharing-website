// Prefill the password field with a randomly generated password
function fillPassword () {
    var randomString = Math.random().toString(36).slice(-11);
    document.getElementById("password").value = randomString;
}

function fillDate () {
    // Prefill the date picker with a date that is a week from today.
    var oneWeek = getFutureDate(7);
    oneWeek = getDateFormatted(oneWeek);
    document.getElementById('expiryDate').value = oneWeek;

    // Set the min date for the date picker to today so that the user cannot select past dates.
    var minDate = getFutureDate(1)
    minDate = getDateFormatted(minDate)
    document.getElementById("expiryDate").min = minDate;    
}

// Pass in an int to add that number of days to the current date
function getFutureDate(additionalDays) {
    var date = new Date();
    date.setDate(date.getDate() + additionalDays);
    return date;
}

// Pass in a date variable in order to receive a nicly formatted string which can be used in the HTML.
function getDateFormatted(date) {
    return date.getFullYear().toString().padStart(4, '0') + '-' + (date.getMonth()+1).toString().padStart(2, '0') + '-' + date.getDate().toString().padStart(2, '0');
}

// Function run when the page is loaded
window.onload = function() {
    // Hide the alert
    $("#expiryAlert").hide();
    fillPassword();
    fillDate();
}

// This function is run when the form is submitted.
function checkForPastDate() {
    // Rehide the alert so that the alert is only shown when there is a problem with the entered expiry date
    $("#expiryAlert").hide();
    
    var inputDate = new Date(document.getElementById("expiryDate").value);
    var currentDate = new Date();
    
    if(inputDate < currentDate){
        $("#expiryAlert").show();
    }
  }