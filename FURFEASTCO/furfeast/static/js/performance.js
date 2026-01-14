// Performance monitoring for FurFeast
(function() {
    'use strict';
    
    // Track page load performance
    function trackPerformance() {
        if ('performance' in window && 'timing' in performance) {
            const timing = performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;
            const domReady = timing.domContentLoadedEventEnd - timing.navigationStart;
            
            // Log performance metrics (remove in production)
            if (window.location.hostname === 'localhost' || window.location.hostname.includes('127.0.0.1')) {
                console.log(`🐾 FurFeast Performance:
                    - Page Load Time: ${loadTime}ms
                    - DOM Ready: ${domReady}ms
                    - Target: <2000ms
                    - Status: ${loadTime < 2000 ? '✅ GOOD' : '⚠️ NEEDS OPTIMIZATION'}`);
            }
        }
    }
    
    // Track when page is fully loaded
    if (document.readyState === 'complete') {
        trackPerformance();
    } else {
        window.addEventListener('load', trackPerformance);
    }
    
    // Track Core Web Vitals if available
    if ('PerformanceObserver' in window) {
        try {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.entryType === 'largest-contentful-paint') {
                        const lcp = entry.startTime;
                        if (window.location.hostname === 'localhost' || window.location.hostname.includes('127.0.0.1')) {
                            console.log(`🎯 LCP: ${Math.round(lcp)}ms (Target: <2500ms)`);
                        }
                    }
                }
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {
            // PerformanceObserver not supported
        }
    }
})();