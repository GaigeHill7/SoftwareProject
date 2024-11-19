document.getElementById("Movie-Buy-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from refreshing the page

    const Movie = document.getElementById("Movie").value;
    const TicketNum = document.getElementById("TicketNum").value;
    const email = document.getElementById("email").value;
    const cardNum = document.getElementById("CardNum").value;
    const CVV = document.getElementById("CVV").value;
    const Exp = document.getElementById("Exp").value;

    //Need to confirm movie is showing DB

    //Need to confirm purchase was successful and figure out how to display and store code
});