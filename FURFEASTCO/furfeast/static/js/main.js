// Optimized Main FurFeast Logic with performance improvements

// Cache DOM elements
const domCache = new Map();

function getCachedElement(id) {
    if (!domCache.has(id)) {
        domCache.set(id, document.getElementById(id));
    }
    return domCache.get(id);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Optimized Toast Notification System
let toastContainer = null;

function getToastContainer() {
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;pointer-events:none';
        document.body.appendChild(toastContainer);
    }
    return toastContainer;
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.style.pointerEvents = 'auto';
    
    const icon = type === 'success' ? '🐾' : type === 'error' ? '⚠️' : '🔔';
    
    // Create structure safely
    const container = document.createElement('div');
    container.style.cssText = 'display: flex; align-items: center; gap: 12px;';
    
    const iconSpan = document.createElement('span');
    iconSpan.style.fontSize = '20px';
    iconSpan.textContent = icon;
    
    const textDiv = document.createElement('div');
    
    const titleDiv = document.createElement('div');
    titleDiv.style.cssText = 'font-weight: 600; margin-bottom: 2px;';
    titleDiv.textContent = 'FurFeast';
    
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = 'font-size: 14px; opacity: 0.9;';
    messageDiv.textContent = message;
    
    textDiv.appendChild(titleDiv);
    textDiv.appendChild(messageDiv);
    container.appendChild(iconSpan);
    container.appendChild(textDiv);
    toast.appendChild(container);
    
    getToastContainer().appendChild(toast);
    
    requestAnimationFrame(() => toast.classList.add('show'));
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// FurFeast Custom Confirm Modal
function showConfirm(message, onConfirm) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    
    // Create modal structure safely
    const modal = document.createElement('div');
    modal.className = 'modal';
    
    const contentDiv = document.createElement('div');
    contentDiv.style.cssText = 'text-align: center; margin-bottom: 20px;';
    
    const iconDiv = document.createElement('div');
    iconDiv.style.cssText = 'font-size: 48px; margin-bottom: 12px;';
    iconDiv.textContent = '🐾';
    
    const titleH3 = document.createElement('h3');
    titleH3.style.cssText = 'font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 8px;';
    titleH3.textContent = 'FurFeast';
    
    const messageP = document.createElement('p');
    messageP.style.cssText = 'color: #64748b; font-size: 14px;';
    messageP.textContent = message;
    
    const buttonsDiv = document.createElement('div');
    buttonsDiv.style.cssText = 'display: flex; gap: 12px; justify-content: center;';
    
    const cancelBtn = document.createElement('button');
    cancelBtn.style.cssText = 'padding: 10px 20px; background: #e2e8f0; color: #475569; border: none; border-radius: 8px; font-weight: 500; cursor: pointer;';
    cancelBtn.textContent = 'Cancel';
    
    const confirmBtn = document.createElement('button');
    confirmBtn.style.cssText = 'padding: 10px 20px; background: #f97316; color: white; border: none; border-radius: 8px; font-weight: 500; cursor: pointer;';
    confirmBtn.textContent = 'Confirm';
    
    // Assemble structure
    contentDiv.appendChild(iconDiv);
    contentDiv.appendChild(titleH3);
    contentDiv.appendChild(messageP);
    buttonsDiv.appendChild(cancelBtn);
    buttonsDiv.appendChild(confirmBtn);
    modal.appendChild(contentDiv);
    modal.appendChild(buttonsDiv);
    overlay.appendChild(modal);
    
    document.body.appendChild(overlay);
    
    const closeModal = () => {
        overlay.classList.remove('show');
        setTimeout(() => {
            if (overlay.parentNode) {
                document.body.removeChild(overlay);
            }
        }, 300);
    };
    
    cancelBtn.addEventListener('click', closeModal);
    confirmBtn.addEventListener('click', () => {
        onConfirm();
        closeModal();
    });
    
    requestAnimationFrame(() => overlay.classList.add('show'));
}

// Optimized API calls with error handling
async function makeApiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (response.headers.get('content-type')?.includes('text/html') && response.url.includes('login')) {
            window.location.href = '/login/';
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

async function addToCart(productId) {
    try {
        const data = await makeApiCall(`/api/cart/add/${productId}/`, {
            method: 'POST'
        });

        if (data && data.status === 'success') {
            updateCartBadge(data.cart_count);
            if (data.wishlist_count !== undefined) {
                updateWishlistBadge(data.wishlist_count);
            }
            showToast(data.message, 'success');
        } else if (data && data.status === 'error') {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('Failed to add item to cart', 'error');
    }
}

async function addToWishlist(productId) {
    try {
        const data = await makeApiCall(`/api/wishlist/add/${productId}/`, {
            method: 'POST'
        });

        if (data && data.status === 'success') {
            updateWishlistBadge(data.wishlist_count);
            if (data.cart_count !== undefined) {
                updateCartBadge(data.cart_count);
            }
            showToast(data.message, 'success');
        }
    } catch (error) {
        showToast('Failed to add item to wishlist', 'error');
    }
}

// Helper functions to update badges
function updateCartBadge(count) {
    const badge = getCachedElement('cart-badge');
    if (badge) {
        badge.textContent = count;
        badge.classList.toggle('opacity-0', count <= 0);
        badge.classList.toggle('opacity-100', count > 0);
    }
}

function updateWishlistBadge(count) {
    const badge = getCachedElement('wishlist-badge');
    if (badge) {
        badge.textContent = count;
        badge.classList.toggle('opacity-0', count <= 0);
        badge.classList.toggle('opacity-100', count > 0);
    }
}

// Optimized DOM ready handler
function onDOMReady(callback) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', callback);
    } else {
        callback();
    }
}

onDOMReady(() => {
    // Optimized search input handling with debouncing
    const searchInput = document.querySelector('input[type="text"]');
    if (searchInput) {
        let timeout;
        const handleFocus = () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                searchInput.parentElement.classList.add('scale-[1.02]');
            }, 50);
        };
        const handleBlur = () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                searchInput.parentElement.classList.remove('scale-[1.02]');
            }, 50);
        };
        
        searchInput.addEventListener('focus', handleFocus, { passive: true });
        searchInput.addEventListener('blur', handleBlur, { passive: true });
    }
});