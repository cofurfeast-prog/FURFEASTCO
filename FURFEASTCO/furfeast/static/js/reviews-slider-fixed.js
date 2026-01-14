// Infinite loop reviews slider
let currentReviewIndex = 0;
let totalReviews = 0;
let isTransitioning = false;

function initReviewsSlider() {
    const slider = document.getElementById('reviewsSlider');
    const prevBtn = document.getElementById('prevReview');
    const nextBtn = document.getElementById('nextReview');
    
    if (!slider) return;
    
    totalReviews = slider.children.length;
    
    // Clone first and last reviews for infinite effect
    const firstClone = slider.children[0].cloneNode(true);
    const lastClone = slider.children[totalReviews - 1].cloneNode(true);
    
    slider.appendChild(firstClone);
    slider.insertBefore(lastClone, slider.children[0]);
    
    // Start at first real review (index 1 because of clone)
    currentReviewIndex = 1;
    slider.style.transform = `translateX(-100%)`;
    
    // Show buttons if more than 1 review
    const showButtons = totalReviews > 1;
    if (prevBtn) prevBtn.style.display = showButtons ? 'block' : 'none';
    if (nextBtn) nextBtn.style.display = showButtons ? 'block' : 'none';
    
    // Click events
    if (nextBtn) {
        nextBtn.onclick = () => nextSlide();
    }
    
    if (prevBtn) {
        prevBtn.onclick = () => prevSlide();
    }
    
    // Auto slide every 6 seconds
    if (totalReviews > 1) {
        setInterval(nextSlide, 6000);
    }
}

function nextSlide() {
    if (isTransitioning) return;
    
    const slider = document.getElementById('reviewsSlider');
    if (!slider) return;
    
    isTransitioning = true;
    currentReviewIndex++;
    
    slider.style.transition = 'transform 0.5s ease-in-out';
    slider.style.transform = `translateX(-${currentReviewIndex * 100}%)`;
    
    // If we're at the cloned first slide, jump to real first slide
    if (currentReviewIndex === totalReviews + 1) {
        setTimeout(() => {
            slider.style.transition = 'none';
            currentReviewIndex = 1;
            slider.style.transform = `translateX(-100%)`;
            setTimeout(() => {
                slider.style.transition = 'transform 0.5s ease-in-out';
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
    
    const slider = document.getElementById('reviewsSlider');
    if (!slider) return;
    
    isTransitioning = true;
    currentReviewIndex--;
    
    slider.style.transition = 'transform 0.5s ease-in-out';
    slider.style.transform = `translateX(-${currentReviewIndex * 100}%)`;
    
    // If we're at the cloned last slide, jump to real last slide
    if (currentReviewIndex === 0) {
        setTimeout(() => {
            slider.style.transition = 'none';
            currentReviewIndex = totalReviews;
            slider.style.transform = `translateX(-${totalReviews * 100}%)`;
            setTimeout(() => {
                slider.style.transition = 'transform 0.5s ease-in-out';
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