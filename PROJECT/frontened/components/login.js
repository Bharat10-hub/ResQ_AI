document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const username = document.getElementById("inputVal").value
    

    if (username) {
        localStorage.setItem("username", JSON.stringify(username));
        window.location.href = "index.html";
    } else {
        alert("Please enter a valid username and password.");
    }
});
