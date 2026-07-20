// include.js

function loadHTML(id, file) {
    fetch(file)
        .then(response => response.text())
        .then(data => {
            document.getElementById(id).innerHTML = data;
        });
}

// Load header and footer
document.addEventListener("DOMContentLoaded", function() {
    loadHTML("header", "header.html");
    loadHTML("footer", "footer.html");
});


