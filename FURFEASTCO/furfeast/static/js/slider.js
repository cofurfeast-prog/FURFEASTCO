// Fixed Height Enforcement
function ensureHeroSliderFixedHeight() {
    const slider = document.getElementById('hero-slider');
    if (!slider) return;
    
    // Remove any conflicting styles
    slider.style.aspectRatio = '';
    slider.style.height = '';
    
    // Set fixed height based on screen size
    if (window.innerWidth < 640) {
        slider.style.height = '500px';
    } else if (window.innerWidth < 1024) {
        slider.style.height = '600px';
    } else {
        slider.style.height = '700px';
    }
    
    // Lock the dimensions
    Object.assign(slider.style, {
        minHeight: slider.style.height,
        maxHeight: slider.style.height,
        overflow: 'hidden'
    });
}

// Call immediately
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureHeroSliderFixedHeight);
} else {
    ensureHeroSliderFixedHeight();
}

// Update on resize
window.addEventListener('resize', ensureHeroSliderFixedHeight);

// Hero Slider - Dynamic from database
let slides = [];
let currentSlide = 0;
const sliderContainer = document.getElementById('hero-slider');

// Fallback slides
const fallbackSlides = [
  {
    image: "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=1920&h=800&fit=crop",
    headline: "Nutrition That Shows",
    subheadline: "Premium pet food for healthier, happier companions",
    cta_text: "Shop Now",
    cta_link: "/shop/",
    align: "left",
  },
  {
    image: "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=1920&h=800&fit=crop",
    headline: "Because They're Family",
    subheadline: "Grain-free, vet-approved formulas for every life stage",
    cta_text: "Explore Cat Food",
    cta_link: "/shop/?category=cat-food",
    align: "right",
  },
  {
    image: "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=1920&h=800&fit=crop",
    headline: "Everything They Need",
    subheadline: "Premium accessories for happy, healthy pets",
    cta_text: "Browse Accessories",
    cta_link: "/accessories/",
    align: "left",
  },
];

// Combine database images with fallback images
if (typeof heroImages !== 'undefined' && heroImages.length >= 3) {
  slides = heroImages;
} else if (typeof heroImages !== 'undefined' && heroImages.length > 0) {
  slides = [...heroImages, ...fallbackSlides];
} else {
  slides = fallbackSlides;
}

function renderSlides() {
  if (!sliderContainer) return;

  // Clear container
  sliderContainer.innerHTML = '';

  // Create slides using DOM methods
  slides.forEach((slide, index) => {
    const isMobile = window.innerWidth <= 768;
    const selectedImage = isMobile ? (slide.mobile_image || slide.image) : (slide.desktop_image || slide.image);
    
    // Create slide container
    const slideDiv = document.createElement('div');
    slideDiv.className = 'slide-item absolute inset-0 transition-opacity duration-1000 ease-in-out opacity-0';
    slideDiv.dataset.index = index;
    
    // Background
    const bgDiv = document.createElement('div');
    bgDiv.className = 'absolute inset-0 bg-slate-200';
    slideDiv.appendChild(bgDiv);
    
    // Image
    const img = document.createElement('img');
    img.src = selectedImage;
    img.alt = slide.headline;
    img.className = 'absolute inset-0 w-full h-full object-cover object-center';
    img.loading = 'eager';
    img.decoding = 'sync';
    
    // ADD explicit styles
    Object.assign(img.style, {
        position: 'absolute',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        objectPosition: 'center',
        display: 'block'
    });
    
    slideDiv.appendChild(img);
    
    // Gradient overlay
    const gradientDiv = document.createElement('div');
    gradientDiv.className = 'absolute inset-0 bg-gradient-to-r from-black/60 via-black/30 to-transparent';
    slideDiv.appendChild(gradientDiv);
    
    // Content container
    const contentDiv = document.createElement('div');
    contentDiv.className = 'container-wide relative h-full flex items-center px-4 sm:px-6 lg:px-12';
    
    const textDiv = document.createElement('div');
    textDiv.className = `max-w-xl ${slide.align === 'right' ? 'ml-auto text-right' : 'mr-auto text-left'}`;
    textDiv.style.transform = `translateY(${((slide.text_position_y || 50) - 50) * 0.5}%)`;
    
    // Headline
    const h1 = document.createElement('h1');
    h1.className = 'text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white mb-4 leading-tight animate-slide-up';
    h1.style.animationDelay = '100ms';
    h1.textContent = slide.headline;
    textDiv.appendChild(h1);
    
    // Subheadline
    const p = document.createElement('p');
    p.className = `text-lg sm:text-xl text-white/90 mb-6 sm:mb-8 animate-slide-up typewriter-${index}`;
    p.style.animationDelay = '200ms';
    p.textContent = slide.subheadline;
    textDiv.appendChild(p);
    
    // CTA button
    const a = document.createElement('a');
    a.href = slide.cta_link;
    a.className = 'inline-block btn-primary text-base sm:text-lg shadow-glow hover:scale-105 transition-transform animate-slide-up';
    a.style.animationDelay = '300ms';
    a.style.backgroundColor = '#3A5A40';
    a.style.color = '#ffffff';
    a.style.padding = '0.75rem 1.5rem';
    a.textContent = slide.cta_text;
    textDiv.appendChild(a);
    
    contentDiv.appendChild(textDiv);
    slideDiv.appendChild(contentDiv);
    sliderContainer.appendChild(slideDiv);
  });

  // Add navigation dots
  const dotsContainer = document.createElement('div');
  dotsContainer.className = 'absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-3 z-20';
  
  slides.forEach((_, index) => {
    const button = document.createElement('button');
    button.className = `w-3 h-3 rounded-full transition-all ${index === 0 ? 'bg-white w-8' : 'bg-white/50'}`;
    button.dataset.slide = index;
    dotsContainer.appendChild(button);
  });
  
  sliderContainer.appendChild(dotsContainer);
  updateSlideVisibility();
}

function updateSlideVisibility() {
  const slideElements = document.querySelectorAll('.slide-item');
  const dots = document.querySelectorAll('[data-slide]');

  slideElements.forEach((el, index) => {
    if (index === currentSlide) {
      el.classList.add('opacity-100', 'z-10');
      el.classList.remove('opacity-0', 'z-0');
      
      // Trigger typewriter animation for all devices
      const typewriterEl = el.querySelector(`[class*="typewriter-"]`);
      if (typewriterEl) {
        typewriterEl.style.animation = 'none';
        typewriterEl.offsetHeight; // Trigger reflow
        
        // Different timing for mobile vs desktop
        const isMobile = window.innerWidth <= 640;
        const duration = isMobile ? '4s' : '6s';
        const steps = isMobile ? 50 : 60;
        
        typewriterEl.style.animation = `typing ${duration} steps(${steps}, end)`;
        typewriterEl.style.width = '100%';
      }
    } else {
      el.classList.add('opacity-0', 'z-0');
      el.classList.remove('opacity-100', 'z-10');
    }
  });

  dots.forEach((dot, index) => {
    if (index === currentSlide) {
      dot.classList.add('bg-white', 'w-8');
      dot.classList.remove('bg-white/50');
    } else {
      dot.classList.remove('bg-white', 'w-8');
      dot.classList.add('bg-white/50');
    }
  });
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  updateSlideVisibility();
}

if (sliderContainer) {
  renderSlides();

  // Dot click navigation
  const dots = document.querySelectorAll('[data-slide]');
  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      currentSlide = parseInt(dot.dataset.slide);
      updateSlideVisibility();
    });
  });

  // Auto-slide every 5 seconds
  setInterval(nextSlide, 5000);
}
