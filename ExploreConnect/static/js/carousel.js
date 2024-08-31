document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.querySelector('.carousel-items');
    const items = document.querySelectorAll('.carousel-item');
    let currentIndex = 0;
    const intervalTime = 3000; // 3 seconds

    function showNextItem() {
        currentIndex = (currentIndex + 1) % items.length;
        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    setInterval(showNextItem, intervalTime);
});
