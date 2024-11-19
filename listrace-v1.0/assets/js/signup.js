document.getElementById("user-signup-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form from refreshing the page

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;
    const phoneNumber = document.getElementById("phonenumber").value;

    // Logic to check if email or username already in DB
    alert("Login successful! Redirecting to admin dashboard...");

    //Need to be confirmed that it was put into DB
    window.location.href = "index.html"; // Redirect to homepage
   
});