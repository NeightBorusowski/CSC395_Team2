$(document).ready(function(){
    $("#hamburger").click(function () {
        $("#navbar").toggleClass("visible");
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById("popup");
    const closeBtn = document.querySelector(".close-btn");

    // Handle form submit event
    function handleSubmit(event) {
        event.preventDefault(); // Prevent default form submission behavior
        showPopup();
    }

    // Show popup
    function showPopup() {
        popup.classList.remove("hidden");
        popup.classList.add("active");
    }

    // Hide popup
    function hidePopup() {
        popup.classList.remove("active");
        popup.classList.add("hidden");
    }

    // Close popup when close button is clicked
    closeBtn.addEventListener("click", function() {
        hidePopup();
    });

    // Expose handleSubmit function to the global scope
    window.handleSubmit = handleSubmit;
});