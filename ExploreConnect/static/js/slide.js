document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slide');
    
    function showSlides() {
        slides.forEach((slide, index) => {
            slide.style.display = 'none';
            if (index === slideIndex) {
                slide.style.display = 'block';
            }
        });
        slideIndex = (slideIndex + 1) % slides.length;
        setTimeout(showSlides, 3000); // Change slide every 3 seconds
    }
    
    showSlides();
});
