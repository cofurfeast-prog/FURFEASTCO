// Admin validation with FurFeast modal
document.addEventListener('DOMContentLoaded', function() {
    // Check for validation errors on page load
    const errorList = document.querySelector('.errorlist');
    if (errorList) {
        const errorText = errorList.textContent;
        if (errorText.includes('Cannot mark item as out of stock')) {
            showFurFeastModal('Stock Validation Error', errorText);
        }
    }
    
    // Add form submission validation
    const form = document.querySelector('#product_form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const isOutOfStock = document.querySelector('#id_is_out_of_stock');
            const stock = document.querySelector('#id_stock');
            
            if (isOutOfStock && stock && isOutOfStock.checked && parseInt(stock.value) > 0) {
                e.preventDefault();
                showFurFeastModal('Stock Validation Error', 'Cannot mark item as out of stock when stock quantity is greater than 0.');
                return false;
            }
        });
    }
});

function showFurFeastModal(title, message) {
    // Remove existing modal if any
    const existingModal = document.querySelector('.furfeast-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'furfeast-modal';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    // Create modal content
    const modal = document.createElement('div');
    modal.style.cssText = `
        background: white;
        border-radius: 20px;
        padding: 30px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.3s ease;
    `;
    
    modal.innerHTML = `
        <div style="font-size: 48px; margin-bottom: 16px;">🐾</div>
        <h3 style="font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 12px; font-family: 'Nunito', sans-serif;">FurFeast</h3>
        <h4 style="font-size: 16px; font-weight: 600; color: #dc2626; margin-bottom: 8px;">${title}</h4>
        <p style="color: #64748b; font-size: 14px; margin-bottom: 24px; line-height: 1.5;">${message}</p>
        <button onclick="closeFurFeastModal()" style="
            padding: 12px 24px;
            background: #f97316;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        " onmouseover="this.style.background='#ea580c'" onmouseout="this.style.background='#f97316'">
            Got it!
        </button>
    `;
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

function closeFurFeastModal() {
    const modal = document.querySelector('.furfeast-modal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

// Add fadeOut animation
const fadeOutStyle = document.createElement('style');
fadeOutStyle.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(fadeOutStyle);