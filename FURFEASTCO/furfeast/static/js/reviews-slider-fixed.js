// Infinite loop reviews slider with no gaps
let currentReviewIndex = 0;
let totalReviews = 0;
let isTransitioning = false;
let reviewWidth = 0;
let visibleReviews = 1;

function initReviewsSlider() {
    const slider = document.getElementById('reviewsSlider');
    const prevBtn = document.getElementById('prevReview');
    const nextBtn = document.getElementById('nextReview');
    
    if (!slider) return;
    
    const originalReviews = Array.from(slider.children);
    totalReviews = originalReviews.length;
    
    if (totalReviews === 0) return;
    
    // Determine visible reviews based on screen size
    function updateVisibleReviews() {
        if (window.innerWidth >= 1024) {
            visibleReviews = 3;
        } else if (window.innerWidth >= 768) {
            visibleReviews = 2;
        } else {
            visibleReviews = 1;
        }
    }
    
    updateVisibleReviews();
    
    // Clone all reviews 3 times for seamless loop
    slider.innerHTML = '';
    for (let i = 0; i < 3; i++) {
        originalReviews.forEach(review => {
            slider.appendChild(review.cloneNode(true));
        });
    }
    
    // Start at middle set
    currentReviewIndex = totalReviews;
    updateSliderPosition(false);
    
    // Show buttons if more than visible reviews
    const showButtons = totalReviews > visibleReviews;
    if (prevBtn) prevBtn.style.display = showButtons ? 'block' : 'none';
    if (nextBtn) nextBtn.style.display = showButtons ? 'block' : 'none';
    
    // Click events
    if (nextBtn) {
        nextBtn.onclick = () => nextSlide();
    }
    
    if (prevBtn) {
        prevBtn.onclick = () => prevSlide();
    }
    
    // Auto slide every 5 seconds
    if (totalReviews > visibleReviews) {
        setInterval(nextSlide, 5000);
    }
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            updateVisibleReviews();
            updateSliderPosition(false);
        }, 250);
    });
}

function updateSliderPosition(animate = true) {
    const slider = document.getElementById('reviewsSlider');
    if (!slider) return;
    
    const slideWidth = 100 / visibleReviews;
    const offset = currentReviewIndex * slideWidth;
    
    slider.style.transition = animate ? 'transform 0.5s ease-in-out' : 'none';
    slider.style.transform = `translateX(-${offset}%)`;
}

function nextSlide() {
    if (isTransitioning) return;
    
    isTransitioning = true;
    currentReviewIndex++;
    
    updateSliderPosition(true);
    
    // Reset to middle set when reaching end
    if (currentReviewIndex >= totalReviews * 2) {
        setTimeout(() => {
            currentReviewIndex = totalReviews;
            updateSliderPosition(false);
            setTimeout(() => {
                isTransitioning = false;
            }, 50);
        }, 500);
    } else {
        setTimeout(() => {
            isTransitioning = false;
        }, 500);
    }
}

function prevSlide() {
    if (isTransitioning) return;
    
    isTransitioning = true;
    currentReviewIndex--;
    
    updateSliderPosition(true);
    
    // Reset to middle set when reaching start
    if (currentReviewIndex < totalReviews) {
        setTimeout(() => {
            currentReviewIndex = totalReviews * 2 - 1;
            updateSliderPosition(false);
            setTimeout(() => {
                isTransitioning = false;
            }, 50);
        }, 500);
    } else {
        setTimeout(() => {
            isTransitioning = false;
        }, 500);
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReviewsSlider);
} else {
    initReviewsSlider();
}