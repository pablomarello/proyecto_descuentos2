  const sliderContainer = document.getElementById('sliderContainer');
  let scrollPosition = 0;

  function handleScroll(direction) {
      const scrollAmount = 300;
      if (direction === 'left') {
          scrollPosition = Math.max(0, scrollPosition - scrollAmount);
      } else {
          scrollPosition = Math.min(
              sliderContainer.scrollWidth - sliderContainer.clientWidth,
              scrollPosition + scrollAmount
          );
      }
      
      sliderContainer.scrollTo({
          left: scrollPosition,
          behavior: 'smooth'
      });
  }

  window.addEventListener('resize', () => {
      scrollPosition = sliderContainer.scrollLeft;
  });