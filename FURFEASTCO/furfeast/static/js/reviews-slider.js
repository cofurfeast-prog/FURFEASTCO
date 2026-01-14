// Reviews Slider - Responsive and Touch-friendly
class ReviewsSlider {
    constructor() {
        this.currentIndex = 0;
        this.slider = document.getElementById('reviewsSlider');
        this.prevBtn = document.getElementById('prevReview');
        this.nextBtn = document.getElementById('nextReview');
        this.autoSlideInterval = null;
        
        if (!this.slider) return;
        
        this.init();
    }
    
    init() {
        this.updateResponsiveSettings();
        this.bindEvents();
        this.startAutoSlide();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                this.updateResponsiveSettings();
                this.showSlide(this.currentIndex);
            }, 250);
        });
    }
    
    updateResponsiveSettings() {
        const width = window.innerWidth;
        this.reviewsPerView = width >= 1024 ? 3 : (width >= 768 ? 2 : 1);
        this.totalReviews = this.slider.children.length;
        this.maxIndex = Math.max(0, this.totalReviews - this.reviewsPerView);
        
        // Update button visibility
        const showButtons = this.totalReviews > this.reviewsPerView;
        if (this.prevBtn) this.prevBtn.style.display = showButtons ? 'block' : 'none';
        if (this.nextBtn) this.nextBtn.style.display = showButtons ? 'block' : 'none';
        
        // Reset index if needed
        if (this.currentIndex > this.maxIndex) {
            this.currentIndex = this.maxIndex;
        }
    }
    
    bindEvents() {
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.nextSlide());
        }
        
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prevSlide());
        }
        
        // Touch/swipe support
        let startX = 0;
        let isDragging = false;
        
        this.slider.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
            this.stopAutoSlide();
        }, { passive: true });
        
        this.slider.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
        }, { passive: false });
        
        this.slider.addEventListener('touchend', (e) => {
            if (!isDragging) return;
            isDragging = false;
            
            const endX = e.changedTouches[0].clientX;
            const diff = startX - endX;
            
            if (Math.abs(diff) > 50) { // Minimum swipe distance
                if (diff > 0) {
                    this.nextSlide();
                } else {
                    this.prevSlide();
                }
            }
            
            this.startAutoSlide();
        }, { passive: true });
        
        // Mouse drag support for desktop
        let mouseStartX = 0;
        let isMouseDragging = false;
        
        this.slider.addEventListener('mousedown', (e) => {
            mouseStartX = e.clientX;
            isMouseDragging = true;
            this.stopAutoSlide();
            e.preventDefault();
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isMouseDragging) return;
            e.preventDefault();
        });
        
        document.addEventListener('mouseup', (e) => {
            if (!isMouseDragging) return;
            isMouseDragging = false;
            
            const diff = mouseStartX - e.clientX;
            
            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    this.nextSlide();
                } else {\n                    this.prevSlide();\n                }\n            }\n            \n            this.startAutoSlide();\n        });\n    }\n    \n    showSlide(index) {\n        if (!this.slider || this.totalReviews <= this.reviewsPerView) return;\n        \n        // Ensure index is within bounds\n        this.currentIndex = Math.max(0, Math.min(index, this.maxIndex));\n        \n        const slideWidth = 100 / this.reviewsPerView;\n        const translateX = -this.currentIndex * slideWidth;\n        \n        this.slider.style.transform = `translateX(${translateX}%)`;\n        \n        // Update button states\n        if (this.prevBtn) {\n            this.prevBtn.disabled = this.currentIndex <= 0;\n            this.prevBtn.style.opacity = this.currentIndex <= 0 ? '0.5' : '1';\n        }\n        \n        if (this.nextBtn) {\n            this.nextBtn.disabled = this.currentIndex >= this.maxIndex;\n            this.nextBtn.style.opacity = this.currentIndex >= this.maxIndex ? '0.5' : '1';\n        }\n    }\n    \n    nextSlide() {\n        if (this.currentIndex >= this.maxIndex) {\n            this.currentIndex = 0; // Loop back to start\n        } else {\n            this.currentIndex++;\n        }\n        this.showSlide(this.currentIndex);\n    }\n    \n    prevSlide() {\n        if (this.currentIndex <= 0) {\n            this.currentIndex = this.maxIndex; // Loop to end\n        } else {\n            this.currentIndex--;\n        }\n        this.showSlide(this.currentIndex);\n    }\n    \n    startAutoSlide() {\n        if (this.totalReviews <= this.reviewsPerView) return;\n        \n        this.stopAutoSlide();\n        this.autoSlideInterval = setInterval(() => {\n            this.nextSlide();\n        }, 5000);\n    }\n    \n    stopAutoSlide() {\n        if (this.autoSlideInterval) {\n            clearInterval(this.autoSlideInterval);\n            this.autoSlideInterval = null;\n        }\n    }\n}\n\n// Initialize when DOM is ready\nif (document.readyState === 'loading') {\n    document.addEventListener('DOMContentLoaded', () => {\n        new ReviewsSlider();\n    });\n} else {\n    new ReviewsSlider();\n}\n