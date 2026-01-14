// Universal Image Adjuster for FurFeast
// Supports both mouse and touch events for desktop and mobile

class ImageAdjuster {
    constructor(inputId, previewContainerId, previewImgId, options = {}) {
        this.inputId = inputId;
        this.previewContainerId = previewContainerId;
        this.previewImgId = previewImgId;
        this.options = {
            maxSize: options.maxSize || 5 * 1024 * 1024, // 5MB default
            allowedTypes: options.allowedTypes || ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
            containerWidth: options.containerWidth || 192, // 48 * 4 = 192px (w-48)
            containerHeight: options.containerHeight || 192,
            showInstructions: options.showInstructions !== false,
            ...options
        };
        
        this.isDragging = false;
        this.startX = 0;
        this.startY = 0;
        this.startLeft = 0;
        this.startTop = 0;
        
        this.init();
    }
    
    init() {
        const input = document.getElementById(this.inputId);
        if (input) {
            input.addEventListener('change', (e) => this.handleFileSelect(e));
        }
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Validate file type
        if (!this.options.allowedTypes.includes(file.type)) {
            this.showError('Please select a valid image file (JPEG, PNG, WebP)');
            event.target.value = '';
            return;
        }
        
        // Validate file size
        if (file.size > this.options.maxSize) {
            this.showError(`File size must be less than ${this.options.maxSize / (1024 * 1024)}MB`);
            event.target.value = '';
            return;
        }
        
        this.previewImage(file);
    }
    
    previewImage(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewContainer = document.getElementById(this.previewContainerId);
            const previewImg = document.getElementById(this.previewImgId);
            
            if (previewImg && previewContainer) {
                previewImg.src = e.target.result;
                previewContainer.classList.remove('hidden');
                
                // Reset position
                previewImg.style.left = '0px';
                previewImg.style.top = '0px';
                
                this.addDragFunctionality(previewImg);
            }
        };
        reader.readAsDataURL(file);
    }
    
    addDragFunctionality(img) {
        // Remove existing listeners
        this.removeDragFunctionality(img);
        
        // Mouse events for desktop
        const mouseDown = (e) => this.startDrag(e.clientX, e.clientY, e);
        const mouseMove = (e) => this.drag(e.clientX, e.clientY, e);
        const mouseUp = () => this.endDrag();
        
        // Touch events for mobile
        const touchStart = (e) => {
            const touch = e.touches[0];
            this.startDrag(touch.clientX, touch.clientY, e);
        };
        const touchMove = (e) => {
            if (e.touches.length > 0) {
                const touch = e.touches[0];
                this.drag(touch.clientX, touch.clientY, e);
            }
        };
        const touchEnd = () => this.endDrag();
        
        // Add event listeners
        img.addEventListener('mousedown', mouseDown);
        document.addEventListener('mousemove', mouseMove);
        document.addEventListener('mouseup', mouseUp);
        
        img.addEventListener('touchstart', touchStart, { passive: false });
        document.addEventListener('touchmove', touchMove, { passive: false });
        document.addEventListener('touchend', touchEnd);
        
        // Store references for cleanup
        img._dragListeners = {
            mouseDown, mouseMove, mouseUp,
            touchStart, touchMove, touchEnd
        };
    }
    
    removeDragFunctionality(img) {
        if (img._dragListeners) {
            const listeners = img._dragListeners;
            img.removeEventListener('mousedown', listeners.mouseDown);
            document.removeEventListener('mousemove', listeners.mouseMove);
            document.removeEventListener('mouseup', listeners.mouseUp);
            
            img.removeEventListener('touchstart', listeners.touchStart);
            document.removeEventListener('touchmove', listeners.touchMove);
            document.removeEventListener('touchend', listeners.touchEnd);
            
            delete img._dragListeners;
        }
    }
    
    startDrag(clientX, clientY, event) {
        this.isDragging = true;
        this.startX = clientX;
        this.startY = clientY;
        
        const img = document.getElementById(this.previewImgId);
        this.startLeft = parseInt(img.style.left) || 0;
        this.startTop = parseInt(img.style.top) || 0;
        
        event.preventDefault();
    }
    
    drag(clientX, clientY, event) {
        if (!this.isDragging) return;
        
        const deltaX = clientX - this.startX;
        const deltaY = clientY - this.startY;
        const newLeft = this.startLeft + deltaX;
        const newTop = this.startTop + deltaY;
        
        const img = document.getElementById(this.previewImgId);
        img.style.left = newLeft + 'px';
        img.style.top = newTop + 'px';
        
        // Store position in hidden inputs if they exist
        const posXInput = document.getElementById('image-pos-x');
        const posYInput = document.getElementById('image-pos-y');
        if (posXInput) posXInput.value = newLeft;
        if (posYInput) posYInput.value = newTop;
        
        event.preventDefault();
    }
    
    endDrag() {
        this.isDragging = false;
    }
    
    showError(message) {
        // Use FurFeast alert if available, otherwise use regular alert
        if (typeof showFurFeastAlert === 'function') {
            showFurFeastAlert(message, 'error');
        } else {
            alert(message);
        }
    }
    
    cancel() {
        const input = document.getElementById(this.inputId);
        const previewContainer = document.getElementById(this.previewContainerId);
        const previewImg = document.getElementById(this.previewImgId);
        
        if (input) input.value = '';
        if (previewContainer) previewContainer.classList.add('hidden');
        if (previewImg) {
            this.removeDragFunctionality(previewImg);
            previewImg.src = '';
        }
        
        // Clear position inputs
        const posXInput = document.getElementById('image-pos-x');
        const posYInput = document.getElementById('image-pos-y');
        if (posXInput) posXInput.value = '0';
        if (posYInput) posYInput.value = '0';
    }
}

// Global function for easy integration
window.createImageAdjuster = function(inputId, previewContainerId, previewImgId, options) {
    return new ImageAdjuster(inputId, previewContainerId, previewImgId, options);
};