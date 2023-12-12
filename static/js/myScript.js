// JavaScript code to calculate and display the year difference
// Restaurant page 
document.addEventListener("DOMContentLoaded", function () {
    // Get all the elements with class "year-difference"
    const yearDifferenceElements = document.querySelectorAll('.year-difference');

    // Loop through each element and calculate the year difference
    yearDifferenceElements.forEach(function (element) {
        const year = parseInt(element.textContent);
        const currentYear = new Date().getFullYear();
        const yearDifference = currentYear - year;

        // Update the content of the element with the year difference
        element.textContent = yearDifference;
    });
});


// Display enlarged image
// Restaurant page
$(document).ready(function () {
    $('.enlargeable').click(function () {
        var imgSrc = $(this).attr('src');
        $('#enlargedImg').attr('src', imgSrc);
        $('#overlay').fadeIn();
        $("section").css({'filter':'blur(5px)'})
    });

    $('#overlay').click(function () {
        $(this).fadeOut();
        $("section").css({'filter':'none'})
    });
});