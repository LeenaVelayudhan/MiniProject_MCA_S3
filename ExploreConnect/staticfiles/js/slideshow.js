document.addEventListener("DOMContentLoaded", function () {
    let slideIndex = 0;
    const slides = document.getElementsByClassName("slideshow-image");
    const totalSlides = slides.length;

    // Function to show the next slide
    function showNextSlide() {
        // Hide all images
        for (let i = 0; i < totalSlides; i++) {
            slides[i].style.display = "none";
        }

        // Increment the slide index and reset if it exceeds the number of slides
        slideIndex++;
        if (slideIndex >= totalSlides) {
            slideIndex = 0;
        }

        // Show the current slide
        slides[slideIndex].style.display = "block";
    }

    // Set an interval to change the slide every 5 seconds
    setInterval(showNextSlide, 5000); // 5000ms = 5 seconds

    
});
