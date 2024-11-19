document.getElementById("admin-login-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form from refreshing the page

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Hardcoded credentials for now
    const adminUsername = "admin";
    const adminPassword = "password123";

    if (username === adminUsername && password === adminPassword) {
        alert("Login successful! Redirecting to admin dashboard...");
        // Redirect to admin page
        window.location.href = "AdminPage.html"; // Replace with your admin page
    } else {
        document.getElementById("error-message").textContent = "Invalid username or password.";
    }
});