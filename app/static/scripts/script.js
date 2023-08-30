function fillPassword () {
    var randomString = Math.random().toString(36).slice(-11);
    document.getElementById("customPassword").value = randomString;
}

function fillDate () {
    
}

window.onload = function() {
    fillPassword();
}