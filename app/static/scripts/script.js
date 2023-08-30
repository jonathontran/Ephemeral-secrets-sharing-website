function fillPassword () {
    var randomString = Math.random().toString(36).slice(-11);
    document.getElementById("password").value = randomString;
}

function fillDate () {
    // Get current date and add 7 days.
    var date = new Date();
    date.setDate(date.getDate() + 7);

    // Converts date to a string which can be input into the HTML
    let oneWeek = date.getFullYear().toString().padStart(4, '0') + '-' + (date.getMonth()+1).toString().padStart(2, '0') + '-' + date.getDate().toString().padStart(2, '0');

    document.getElementById('date').value = oneWeek;


    // Set the min date for the date picker to today so that the user cannot select past dates.
    var today = new Date();
    let minDate = today.getFullYear().toString().padStart(4, '0') + '-' + (today.getMonth()+1).toString().padStart(2, '0') + '-' + today.getDate().toString().padStart(2, '0');

    // Insert the date into the HTML
    document.getElementById("date").min = minDate;    
}

window.onload = function() {
    fillPassword();

    fillDate();
}