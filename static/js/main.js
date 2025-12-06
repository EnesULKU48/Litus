// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
    // AOS Animation initialization
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });
    }
    
    // Initialize cart count
    updateCartCount();
    
    // Initialize event listeners
    initEventListeners();
});

// ==================== EVENT LISTENERS ====================
function initEventListeners() {
    // Add to cart buttons
    document.querySelectorAll('.btn-add-cart').forEach(btn => {
        btn.addEventListener('click', handleAddToCart);
    });
    
    // Like buttons
    document.querySelectorAll('.btn-like').forEach(btn => {
        btn.addEventListener('click', handleLike);
    });
    
    // Favorite buttons
    document.querySelectorAll('#favoriteBtn').forEach(btn => {
        btn.addEventListener('click', handleFavorite);
    });
    
    // Cart quantity controls
    document.querySelectorAll('.increase-qty').forEach(btn => {
        btn.addEventListener('click', handleIncreaseQuantity);
    });
    
    document.querySelectorAll('.decrease-qty').forEach(btn => {
        btn.addEventListener('click', handleDecreaseQuantity);
    });
    
    // Remove from cart
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', handleRemoveFromCart);
    });
    
    // Comment form
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', handleCommentSubmit);
    }
    
    // Checkout button
    const checkoutBtn = document.getElementById('checkoutBtn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', handleCheckout);
    }
    
    // Add to cart from product detail page
    const addToCartBtn = document.getElementById('addToCartBtn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', handleAddToCartFromDetail);
    }
    
    // Like from product detail page
    const likeBtn = document.getElementById('likeBtn');
    if (likeBtn) {
        likeBtn.addEventListener('click', handleLikeFromDetail);
    }
}

// ==================== CART FUNCTIONS ====================
function handleAddToCart(e) {
    e.preventDefault();
    const productId = e.currentTarget.getAttribute('data-product-id');
    addToCart(productId, 1);
}

function handleAddToCartFromDetail(e) {
    e.preventDefault();
    const productId = e.currentTarget.getAttribute('data-product-id');
    const quantity = parseInt(document.getElementById('productQuantity').value) || 1;
    addToCart(productId, quantity);
}

function addToCart(productId, quantity) {
    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId),
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCount();
            showNotification('Ürün sepete eklendi!', 'success');
            
            // Update button state
            const btn = document.querySelector(`[data-product-id="${productId}"].btn-add-cart`);
            if (btn) {
                btn.innerHTML = '<i class="fas fa-check"></i> Eklendi';
                btn.style.backgroundColor = '#28a745';
                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-shopping-bag"></i> Sepete Ekle';
                    btn.style.backgroundColor = '';
                }, 2000);
            }
        } else {
            showNotification('Bir hata oluştu!', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function handleIncreaseQuantity(e) {
    const itemId = e.currentTarget.getAttribute('data-item-id');
    const quantityElement = e.currentTarget.parentElement.querySelector('.quantity-value');
    const currentQuantity = parseInt(quantityElement.textContent);
    updateCartItem(itemId, currentQuantity + 1);
}

function handleDecreaseQuantity(e) {
    const itemId = e.currentTarget.getAttribute('data-item-id');
    const quantityElement = e.currentTarget.parentElement.querySelector('.quantity-value');
    const currentQuantity = parseInt(quantityElement.textContent);
    if (currentQuantity > 1) {
        updateCartItem(itemId, currentQuantity - 1);
    }
}

function updateCartItem(itemId, quantity) {
    fetch('/api/update-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: parseInt(itemId),
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update quantity display
            const quantityElement = document.querySelector(`[data-item-id="${itemId}"] .quantity-value`);
            if (quantityElement) {
                quantityElement.textContent = quantity;
            }
            
            // Update item total
            const cartItem = document.querySelector(`[data-item-id="${itemId}"]`);
            if (cartItem) {
                const priceElement = cartItem.querySelector('.cart-item-price');
                if (priceElement && data.item_total) {
                    priceElement.textContent = data.item_total.toFixed(2) + ' ₺';
                }
            }
            
            // Update cart totals
            if (data.total !== undefined) {
                updateCartTotals(data.total);
            }
            
            if (quantity === 0) {
                // Remove item from DOM
                const cartItem = document.querySelector(`[data-item-id="${itemId}"]`);
                if (cartItem) {
                    cartItem.remove();
                    updateCartCount();
                }
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function handleRemoveFromCart(e) {
    const itemId = e.currentTarget.getAttribute('data-item-id');
    
    if (!confirm('Bu ürünü sepetten çıkarmak istediğinize emin misiniz?')) {
        return;
    }
    
    fetch('/api/remove-from-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: parseInt(itemId)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove item from DOM
            const cartItem = document.querySelector(`[data-item-id="${itemId}"]`);
            if (cartItem) {
                cartItem.style.transition = 'opacity 0.3s';
                cartItem.style.opacity = '0';
                setTimeout(() => {
                    cartItem.remove();
                    updateCartCount();
                    
                    // Check if cart is empty
                    if (data.cart_count === 0) {
                        location.reload();
                    }
                }, 300);
            }
            
            // Update cart totals
            if (data.total !== undefined) {
                updateCartTotals(data.total);
            }
            
            showNotification('Ürün sepetten çıkarıldı!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function updateCartCount() {
    fetch('/cart')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const cartItems = doc.querySelectorAll('.cart-item');
            const count = cartItems.length;
            
            const cartCountElement = document.getElementById('cartCount');
            if (cartCountElement) {
                cartCountElement.textContent = count;
                if (count > 0) {
                    cartCountElement.style.display = 'inline-block';
                } else {
                    cartCountElement.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error updating cart count:', error);
        });
}

function updateCartTotals(total) {
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    
    if (subtotalElement) {
        subtotalElement.textContent = total.toFixed(2) + ' ₺';
    }
    if (totalElement) {
        totalElement.textContent = total.toFixed(2) + ' ₺';
    }
}

function handleCheckout(e) {
    e.preventDefault();
    alert('Bu bir demo sitedir. Ödeme işlemi gerçekleştirilmez.\n\nSiparişiniz başarıyla alındı! (Demo)');
}

// ==================== LIKE FUNCTIONS ====================
function handleLike(e) {
    e.preventDefault();
    const productId = e.currentTarget.getAttribute('data-product-id');
    likeProduct(productId, e.currentTarget);
}

function handleLikeFromDetail(e) {
    e.preventDefault();
    const productId = e.currentTarget.getAttribute('data-product-id');
    likeProduct(productId, e.currentTarget, true);
}

function likeProduct(productId, buttonElement, isDetailPage = false) {
    fetch('/api/like-product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update like count
            if (isDetailPage) {
                const likeCountElement = document.getElementById('likeCount');
                if (likeCountElement) {
                    likeCountElement.textContent = data.likes;
                }
            } else {
                const likeCountElement = buttonElement.querySelector('.like-count');
                if (likeCountElement) {
                    likeCountElement.textContent = data.likes;
                }
            }
            
            // Update button icon
            const icon = buttonElement.querySelector('i');
            if (icon) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                setTimeout(() => {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                }, 500);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// ==================== FAVORITE FUNCTIONS ====================
function handleFavorite(e) {
    e.preventDefault();
    const productId = e.currentTarget.getAttribute('data-product-id');
    toggleFavorite(productId, e.currentTarget);
}

function toggleFavorite(productId, buttonElement) {
    fetch('/api/toggle-favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const icon = buttonElement.querySelector('i');
            if (data.is_favorite) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                showNotification('Favorilere eklendi!', 'success');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                showNotification('Favorilerden çıkarıldı!', 'success');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

// ==================== COMMENT FUNCTIONS ====================
function handleCommentSubmit(e) {
    e.preventDefault();
    const form = e.currentTarget;
    const productId = form.getAttribute('data-product-id');
    const authorName = document.getElementById('commentAuthor').value;
    const content = document.getElementById('commentContent').value;
    
    if (!authorName || !content) {
        showNotification('Lütfen tüm alanları doldurun!', 'error');
        return;
    }
    
    fetch('/api/add-comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId),
            author_name: authorName,
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add comment to DOM
            addCommentToDOM(data.comment);
            
            // Clear form
            form.reset();
            
            showNotification('Yorumunuz eklendi!', 'success');
        } else {
            showNotification(data.message || 'Bir hata oluştu!', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function addCommentToDOM(comment) {
    const commentsList = document.querySelector('.comments-list');
    if (!commentsList) return;
    
    const commentItem = document.createElement('div');
    commentItem.className = 'comment-item';
    commentItem.setAttribute('data-aos', 'fade-up');
    commentItem.innerHTML = `
        <div class="comment-header">
            <strong>${escapeHtml(comment.author_name)}</strong>
            <span class="comment-date">${comment.created_at}</span>
        </div>
        <div class="comment-content">
            ${escapeHtml(comment.content)}
        </div>
    `;
    
    // Insert at the beginning
    if (commentsList.firstChild) {
        commentsList.insertBefore(commentItem, commentsList.firstChild);
    } else {
        commentsList.appendChild(commentItem);
    }
    
    // Reinitialize AOS for new element
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
}

// ==================== UTILITY FUNCTIONS ====================
function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existing = document.querySelector('.custom-notification');
    if (existing) {
        existing.remove();
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `custom-notification alert alert-${type === 'error' ? 'danger' : 'success'}`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== PARALLAX EFFECT ====================
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        const rate = scrolled * 0.5;
        heroSection.style.transform = `translateY(${rate}px)`;
    }
});

// ==================== SMOOTH SCROLL ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

