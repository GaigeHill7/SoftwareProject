document.getElementById("user-login-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from refreshing the page

    const username = document.getElementById("user-username").value;
    const password = document.getElementById("user-password").value;

    // Hardcoded credentials for now
    const userUsername = "user";
    const userPassword = "user123";

    if (username === userUsername && password === userPassword) {
        alert("Login successful! Redirecting to user dashboard...");
        // Redirect to user dashboard page
        window.location.href = "index.html"; // Replace with your actual user dashboard page
    } else {
        document.getElementById("user-error-message").textContent = "Invalid username or password.";
    }
});