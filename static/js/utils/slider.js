    const sliderInner = document.getElementById('slider-inner');
    const images = sliderInner.children;
    let currentIndex = 0;

    document.getElementById('button-next').addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateSlider();
    });

    document.getElementById('button-prev').addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateSlider();
    });

    function updateSlider() {
        const offset = -currentIndex * 100; // Cambia a la posición correcta
        sliderInner.style.transform = `translateX(${offset}%)`;
    }